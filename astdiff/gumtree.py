import logging
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import product
from math import inf
from typing import Dict, List, Set

from more_itertools import first

from astdiff.ast import Node
from astdiff.context import DiffContext, MatchingPair, MatchingSet, NodeId
from astdiff.matcher import Matcher
from astdiff.queue import HeightIndexedPriorityQueue
from astdiff.traversal import post_order_walk, pre_order_walk

logger = logging.getLogger(__name__)

# Constants recommended by Falleri et al.
DEFAULT_MIN_HEIGHT = 2
DEFAULT_MAX_SIZE = 100
DEFAULT_MIN_DICE = 0.5


class GumTreeMatcher(Matcher):
    """
    Implementation of the GumTree node matching algorithm.

    Source: Falleri et al. 2014
    https://hal.archives-ouvertes.fr/hal-01054552/document
    """

    def __init__(
        self,
        min_height: int = DEFAULT_MIN_HEIGHT,
        max_size: int = DEFAULT_MAX_SIZE,
        min_dice: int = DEFAULT_MIN_DICE,
    ):
        self.min_height = min_height
        self.max_size = max_size
        self.min_dice = min_dice

    def find_matching_nodes(
        self,
        source_root: Node,
        target_root: Node,
        context: DiffContext,
    ):
        self.prepare(context)

        self.match_anchors(source_root, target_root)
        self.match_containers(source_root, target_root)

        return self.matching_set

    def prepare(self, context: DiffContext):
        self.context = context
        self.matching_set = MatchingSet()

    def match_anchors(self, source_root: Node, target_root: Node):
        """
        Performs greedy top-down search of the greatest isomorphic subtrees
        between source and target.
        """
        candidate_mappings: List[Mapping] = []

        source_queue = HeightIndexedPriorityQueue()
        source_queue.push(source_root)

        target_queue = HeightIndexedPriorityQueue()
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
                    match = MatchingPair(
                        source=first(mapping.source_ids),
                        target=first(mapping.target_ids),
                    )
                    self.matching_set.update(self._descendant_matches(match))

                # Unmatched nodes are simply skipped since trees have to be of the same
                # height to be isomorphic.
                for mapping in mappings.unmatched_mappings():
                    for source_id in mapping.source_ids:
                        source_queue.open(self.context.source_nodes[source_id])

                    for target_id in mapping.target_ids:
                        target_queue.open(self.context.target_nodes[target_id])

                # Nodes with more than one possible mapping are handled separately.
                candidate_mappings.extend(mappings.candidate_mappings())

        logger.debug("Resolving %s candidate mappings...", len(candidate_mappings))

        # Mappings with more descendants are considered first.
        candidate_mappings.sort(key=lambda x: x.max_size(self.context), reverse=True)

        for mapping in candidate_mappings:
            candidate_matches = sorted(
                (
                    MatchingPair(s, t)
                    for s, t in product(mapping.source_ids, mapping.target_ids)
                ),
                key=self._dice_coefficient,
                reverse=True,
            )

            for match in candidate_matches:
                if not self.matching_set.matched(match):
                    self.matching_set.update(self._descendant_matches(match))

        return self.matching_set

    def match_containers(self, source_root: Node, target_root: Node):
        matches_before = len(self.matching_set)

        for source_node in post_order_walk(source_root):
            candidate_matches = self._find_candidate_container_matches(source_node)
            weighted_candidate_matches = (
                (self._dice_coefficient(x), x) for x in candidate_matches
            )

            dice, match = max(weighted_candidate_matches, default=(-inf, None))
            if dice >= self.min_dice:
                self.matching_set.add(match)
                # TODO: Look for recovery mappings based on min edit distance.

        matches_after = len(self.matching_set)
        logger.debug(
            "Found %s matches during container matching", matches_after - matches_before
        )

        return self.matching_set

    def _find_candidate_container_matches(self, source_node: Node):
        """
        Yields target nodes matched with descendants of given source node.
        """
        seen = set()
        for source_descendant in _descendants(source_node):
            target_id = self.matching_set.source_target_map.get(id(source_descendant))
            if target_id is None:
                continue

            target_node = self.context.target_nodes[target_id]
            while target_node.parent:
                target_node = target_node.parent
                if id(target_node) in seen:
                    break

                target_matched = id(target_node) in self.matching_set.target_source_map
                if not target_matched and source_node.can_match(target_node):
                    yield MatchingPair(id(source_node), id(target_node))

                seen.add(id(target_node))

    def _descendant_matches(self, match: MatchingPair):
        source = self.context.source_nodes[match.source]
        target = self.context.target_nodes[match.target]

        assert source.isomorphic_to(target)
        assert len(source.children) == len(target.children)

        yield match

        for source_child, target_child in zip(source.children, target.children):
            child_match = MatchingPair(id(source_child), id(target_child))
            yield from self._descendant_matches(child_match)

    def _dice_coefficient(self, match: MatchingPair):
        """
        Measures the ratio of common descendants between two nodes.
        """
        source_node = self.context.source_nodes[match.source]
        target_node = self.context.target_nodes[match.target]

        source_node = source_node.parent or source_node
        target_node = target_node.parent or target_node

        source_descendants = set(id(x) for x in _descendants(source_node))
        target_descendants = set(id(x) for x in _descendants(target_node))

        common_descendant_matches = sum(
            self.matching_set.source_target_map.get(x) in target_descendants
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
