import heapq
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from astdiff.ast import Node
from astdiff.context import DiffContext, MatchingPair, NodeId
from astdiff.matcher import Matcher


class GumTreeMatcher(Matcher):
    """
    Implementation of the GumTree node matching algorithm.

    Source: Falleri et al. 2014
    https://hal.archives-ouvertes.fr/hal-01054552/document
    """

    # Constants recommended by Falleri et al.
    MIN_HEIGHT = 2
    MAX_SIZE = 100

    def find_matching_nodes(
        self,
        source_root: Node,
        target_root: Node,
        ctx: DiffContext,
    ):
        first_phase_result = self._top_down_phase(source_root, target_root, ctx)
        second_phase_result = self._bottom_up_phase(source_root, target_root, ctx)
        return frozenset(first_phase_result | second_phase_result)

    def _top_down_phase(
        self,
        source_root: Node,
        target_root: Node,
        ctx: DiffContext,
    ):
        matching_set: Set[MatchingPair] = set()

        candidate_mappings: List[Mapping] = []

        source_queue = HeightIndexedPriorityList()
        source_queue.push(source_root)

        target_queue = HeightIndexedPriorityList()
        target_queue.push(target_root)

        while min(source_queue.peek_max(), target_queue.peek_max()) > self.MIN_HEIGHT:
            if source_queue.peek_max() > target_queue.peek_max():
                for node in source_queue.pop():
                    source_queue.open(node)

            elif source_queue.peek_max() < target_queue.peek_max():
                for node in target_queue.pop():
                    target_queue.open(node)

            else:
                mappings = MappingStore()

                for source_node in source_queue.pop():
                    mappings.add_source(source_node)

                for target_node in target_queue.pop():
                    mappings.add_target(target_node)

                for mapping in mappings.unique_mappings():
                    source_node = ctx.source_nodes[next(iter(mapping.source_ids))]
                    target_node = ctx.target_nodes[next(iter(mapping.target_ids))]
                    matching_set.update(_descendant_matches(source_node, target_node))

                for mapping in mappings.unmatched_mappings():
                    for source_id in mapping.source_ids:
                        source_queue.open(ctx.source_nodes[source_id])

                    for target_id in mapping.target_ids:
                        target_queue.open(ctx.target_nodes[target_id])

                candidate_mappings.extend(mappings.candidate_mappings())

        # TODO: Handle candidate mappings
        return matching_set

    def _bottom_up_phase(
        self,
        source_root: Node,
        target_root: Node,
        ctx: DiffContext,
    ):
        # TODO: Add bottom-up phase
        return set()


def _descendant_matches(source: Node, target: Node):
    assert source.isomorphic_to(target)
    assert len(source.children) == len(target.children)

    yield MatchingPair(
        source=id(source),
        target=id(target),
    )

    for source_child, target_child in zip(source.children, target.children):
        yield from _descendant_matches(source_child, target_child)


@dataclass
class Mapping:
    source_ids: Set[NodeId] = None
    target_ids: Set[NodeId] = None

    def __post_init__(self):
        self.source_ids = self.source_ids or set()
        self.target_ids = self.target_ids or set()

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
        Mappings with more than one node on at least one side.
        """
        return (x for x in self.mappings.values() if not any((x.unique, x.unmatched)))

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
        Pushes children of given node to the heap.
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
