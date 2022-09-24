import heapq
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from functools import partial
from itertools import product
from typing import Dict, List, Set, Tuple

from astdiff.ast import Node
from astdiff.context import DiffContext, MatchingPair, MatchingSet, NodeId
from astdiff.matcher import Matcher
from astdiff.traversal import pre_order_walk

logger = logging.getLogger(__name__)

# Constants recommended by Falleri et al.
DEFAULT_MIN_HEIGHT = 2
DEFAULT_MAX_SIZE = 100


class GumTreeMatcher(Matcher):
    """
    Implementation of the GumTree node matching algorithm.

    Source: Falleri et al. 2014
    https://hal.archives-ouvertes.fr/hal-01054552/document
    """

    def __init__(
        self, min_height: int = DEFAULT_MIN_HEIGHT, max_size: int = DEFAULT_MAX_SIZE
    ):
        self.min_height = min_height
        self.max_size = max_size

    def find_matching_nodes(
        self,
        source_root: Node,
        target_root: Node,
        ctx: DiffContext,
    ):
        anchor_matches = self.match_anchors(source_root, target_root, ctx)
        container_matches = self.match_containers(source_root, target_root, ctx)

        matching_set = MatchingSet()
        matching_set.update(anchor_matches.pairs)
        matching_set.update(container_matches.pairs)

        return matching_set

    def match_anchors(
        self,
        source_root: Node,
        target_root: Node,
        ctx: DiffContext,
    ):
        """
        Performs greedy top-down search of the greatest isomorphic subtrees
        between source and target.
        """
        matching_set = MatchingSet()
        candidate_mappings: List[Mapping] = []

        source_queue = HeightIndexedPriorityList()
        source_queue.push(source_root)

        target_queue = HeightIndexedPriorityList()
        target_queue.push(target_root)

        while min(source_queue.peek_max(), target_queue.peek_max()) >= self.min_height:
            if source_queue.peek_max() > target_queue.peek_max():
                for node in source_queue.pop():
                    source_queue.open(node)

            elif source_queue.peek_max() < target_queue.peek_max():
                for node in target_queue.pop():
                    target_queue.open(node)

            else:
                # Tallest nodes are of the same height, so it is possible that they
                # are also isomorphic.
                mappings = MappingStore()

                for source_node in source_queue.pop():
                    mappings.add_source(source_node)

                for target_node in target_queue.pop():
                    mappings.add_target(target_node)

                # When there's a clear one-to-one mapping between nodes,
                # they can be matched directly. This also implies that their
                # descendants can be matched.
                for mapping in mappings.unique_mappings():
                    source_id = next(iter(mapping.source_ids))
                    target_id = next(iter(mapping.target_ids))
                    matching_set.update(_descendant_matches(source_id, target_id, ctx))

                # Unmatched nodes are simply skipped since trees have to be of the same
                # height to be isomorphic.
                for mapping in mappings.unmatched_mappings():
                    for source_id in mapping.source_ids:
                        source_queue.open(ctx.source_nodes[source_id])

                    for target_id in mapping.target_ids:
                        target_queue.open(ctx.target_nodes[target_id])

                # Nodes with more than one possible mapping are handled separately.
                candidate_mappings.extend(mappings.candidate_mappings())

        logger.debug("Resolving %s candidate mappings...", len(candidate_mappings))

        # Mappings with more descendants are considered first.
        candidate_mappings.sort(key=lambda x: x.max_size(ctx), reverse=True)

        # Candidate matches are given priority based on dice coefficient.
        dice_func = partial(_dice_coefficient, ctx=ctx, matching_set=matching_set)

        # TODO: Consider caching dice coefficient.
        # dice_func = cache(dice_func)

        for mapping in candidate_mappings:
            candidate_matches = (
                MatchingPair(s, t)
                for s, t in product(mapping.source_ids, mapping.target_ids)
            )

            for match in sorted(candidate_matches, key=dice_func, reverse=True):
                if matching_set.unmatched(match):
                    matching_set.update(
                        _descendant_matches(match.source, match.target, ctx)
                    )

        return matching_set

    def match_containers(
        self,
        source_root: Node,
        target_root: Node,
        ctx: DiffContext,
    ):
        # TODO: Add bottom-up phase
        return MatchingSet()


def _descendant_matches(source_id: NodeId, target_id: NodeId, ctx: DiffContext):
    source = ctx.source_nodes[source_id]
    target = ctx.target_nodes[target_id]

    assert source.isomorphic_to(target)
    assert len(source.children) == len(target.children)

    yield MatchingPair(
        source=source_id,
        target=target_id,
    )

    for source_child, target_child in zip(source.children, target.children):
        yield from _descendant_matches(id(source_child), id(target_child), ctx)


def _dice_coefficient(match: MatchingPair, ctx: DiffContext, matching_set: MatchingSet):
    """
    Measures the ratio of common descendants between two nodes.
    """
    source_node = ctx.source_nodes[match.source]
    target_node = ctx.target_nodes[match.target]

    source_node = source_node.parent or source_node
    target_node = target_node.parent or target_node

    source_descendants = set(id(x) for x in _descendants(source_node))
    target_descendants = set(id(x) for x in _descendants(target_node))

    common_descendant_matches = sum(
        matching_set.source_target_map.get(x) in target_descendants
        for x in source_descendants
    )

    return (2 * common_descendant_matches) / (
        len(source_descendants) + len(target_descendants)
    )


def _descendants(node: Node):
    descendants = pre_order_walk(node)
    next(descendants)
    yield from descendants


@dataclass
class Mapping:
    """
    Represents possible mappings between isomorphic nodes.
    """

    source_ids: Set[NodeId] = field(default_factory=set)
    target_ids: Set[NodeId] = field(default_factory=set)

    def max_size(self, context: DiffContext):
        return max(
            context.source_nodes[source_id].metadata.size
            for source_id in self.source_ids
        )

    @property
    def duplicate(self):
        return (
            self.source_ids
            and self.target_ids
            and (len(self.source_ids) > 1 or len(self.target_ids) > 1)
        )

    @property
    def unique(self):
        return len(self.source_ids) == len(self.target_ids) == 1

    @property
    def unmatched(self):
        return not all((self.source_ids, self.target_ids))


class MappingStore:
    """
    Helper class for grouping matching (i.e. isomorphic) nodes.
    """

    def __init__(self):
        self.mappings: Dict[int, Mapping] = defaultdict(Mapping)

    def add_source(self, node: Node):
        self.mappings[node.metadata.hashcode].source_ids.add(id(node))

    def add_target(self, node: Node):
        self.mappings[node.metadata.hashcode].target_ids.add(id(node))

    def candidate_mappings(self):
        """
        Mappings with more than one possible mapping.
        """
        return (x for x in self.mappings.values() if x.duplicate)

    def unique_mappings(self):
        return (x for x in self.mappings.values() if x.unique)

    def unmatched_mappings(self):
        return (x for x in self.mappings.values() if x.unmatched)


class HeightIndexedPriorityList:
    """
    Priority queue that keeps nodes in descending order based on height.
    """

    def __init__(self):
        self.heap: List[Tuple[int, Node]] = []

    def open(self, node: Node):
        """
        Adds children of given node to the heap.
        """
        for child in node.children:
            self.push(child)

    def push(self, node: Node):
        """
        Adds given node to the heap.
        """
        heapq.heappush(self.heap, (-node.metadata.height, node))

    def pop(self):
        """
        Pops all nodes that share the current max height.
        """
        max_height = self.peek_max()
        while self.peek_max() == max_height:
            _, node = heapq.heappop(self.heap)
            yield node

    def peek_max(self):
        """
        Returns height of the tallest node, or 0 if the heap is empty.
        """
        height, _ = (self.heap and self.heap[0]) or (0, None)
        return -height
