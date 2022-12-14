import logging
from functools import partial
from itertools import product
from math import inf
from typing import Callable, List

from more_itertools import first

from astdiff.ast.node import Node
from astdiff.ast.traversal import descendants, post_order_walk, pre_order_walk
from astdiff.context import DiffContext, MatchingPair, MatchingSet
from astdiff.matcher.base import Matcher
from astdiff.matcher.gumtree_utils import Mapping, MappingStore
from astdiff.util import (
    HeightIndexedPriorityQueue,
    group_by,
    longest_common_subsequence,
)

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

    def find_matching_nodes(self, context: DiffContext):
        """
        Generates a matching set using the GumTree algorithm and attaches it to
        the given context.
        """
        self.prepare(context)

        self.match_anchors(context.source_root, context.target_root)
        self.match_containers(context.source_root, context.target_root)

        return self.matching_set

    def prepare(self, context: DiffContext):
        """
        Initializes class members needed for executing the GumTree algorithm and
        binds a new matching set to the given context.
        """
        self.context = context
        self.matching_set = self.context.matching_set = MatchingSet()
        self.dice_cache = {}

    def match_anchors(self, source_root: Node, target_root: Node):
        """
        Performs greedy top-down search of the greatest isomorphic subtrees
        between source and target.

        For a more detailed description, see section 3.1 of the GumTree paper.
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
        # When multiple mappings are possible, break tie using dice coefficient.
        dice_fn = partial(self._dice_coefficient, compare_parents=True)

        for mapping in candidate_mappings:
            candidate_matches = sorted(
                (
                    MatchingPair(s, t)
                    for s, t in product(mapping.source_ids, mapping.target_ids)
                ),
                key=dice_fn,
                reverse=True,
            )

            for match in candidate_matches:
                if not self.matching_set.matched(match):
                    self.matching_set.update(self._descendant_matches(match))

        return self.matching_set

    def match_containers(self, source_root: Node, target_root: Node):
        """
        Implements the bottom-up phase of the GumTree-algorithm.

        For a more detailed description, see section 3.2 of the GumTree paper.
        """
        matches_before = len(self.matching_set)

        for source_node in post_order_walk(source_root):
            if source_node.is_root and self.context.unmatched(source_node):
                match = MatchingPair(id(source_root), id(target_root))
                self._attempt_recovery_matching(match)
                self.matching_set.add(match)

            elif source_node.children and self.context.unmatched(source_node):
                candidate_matches = self._find_candidate_container_matches(source_node)
                weighted_candidate_matches = (
                    (self._dice_coefficient(x), x) for x in candidate_matches
                )

                dice, match = max(weighted_candidate_matches, default=(-inf, None))
                if dice >= self.min_dice:
                    self._attempt_recovery_matching(match)
                    self.matching_set.add(match)

        matches_after = len(self.matching_set)
        logger.debug(
            "Found %s matches during container matching", matches_after - matches_before
        )

        return self.matching_set

    def _attempt_recovery_matching(self, match: MatchingPair):
        """
        Implements recovery matching. That is, tries to find from the children of
        the given nodes new matches that have been missed during previous phases.
        """
        logger.debug("Finding recovery matches...")

        source = self.context.source_nodes[match.source]
        target = self.context.target_nodes[match.target]

        if max(source.metadata.size, target.metadata.size) >= self.max_size:
            logger.debug(
                "Subtrees have size larger than %s, skipping recovery matching...",
                self.max_size,
            )
            return

        self._attempt_longest_common_subsequence_matching(
            source, target, lambda a, b: a.isomorphic_to(b)
        )

        self._attempt_longest_common_subsequence_matching(
            source, target, lambda a, b: a.isomorphic_to_without_values(b)
        )

        self._attempt_histogram_matching(source, target)

    def _attempt_longest_common_subsequence_matching(
        self, source: Node, target: Node, equals_fn: Callable[[Node, Node], bool]
    ):
        """
        Looks for unmatched but matchable subtrees using
        the longest common subsequence algorithm and the given equality function.
        """
        unmatched_source_children = [
            x for x in source.children if self.context.unmatched(x)
        ]
        unmatched_target_children = [
            x for x in target.children if self.context.unmatched(x)
        ]

        for source_child, target_child in longest_common_subsequence(
            unmatched_source_children,
            unmatched_target_children,
            equals_fn,
        ):
            if any(self.context.partner(x) for x in pre_order_walk(source_child)):
                continue
            if any(self.context.partner(x) for x in pre_order_walk(target_child)):
                continue

            child_match = MatchingPair(id(source_child), id(target_child))
            self.matching_set.update(self._descendant_matches(child_match))

    def _attempt_histogram_matching(self, source: Node, target: Node):
        """
        Looks for unmatched but matchable subtrees by searching nodes that have
        an unique label (i.e. type) among their siblings.
        """
        group_by_label = partial(group_by, key_fn=lambda x: x.label)

        source_hist = group_by_label(source.children)
        target_hist = group_by_label(target.children)

        candidate_matches = (
            MatchingPair(
                id(first(source_hist[label])),
                id(first(target_hist[label])),
            )
            for label in source_hist
            if len(source_hist[label]) == len(target_hist[label]) == 1
        )

        for match in candidate_matches:
            if not self.matching_set.matched(match):
                self.matching_set.add(match)
                self._attempt_recovery_matching(match)

    def _find_candidate_container_matches(self, source_tree: Node):
        """
        Yields target nodes matched with descendants of given source node. Used in
        the bottom-up phase of the GumTree algorithm.
        """
        seen = set()
        for source in descendants(source_tree):
            target = self.context.partner(source)
            if target is None:
                continue

            while target.parent:
                target = target.parent
                if id(target) in seen:
                    break

                if not self.context.partner(target) and source_tree.can_match(target):
                    yield MatchingPair(id(source_tree), id(target))

                seen.add(id(target))

    def _descendant_matches(self, match: MatchingPair):
        """
        Yields submatches of trees that share the same structure.
        """
        source = self.context.source_nodes[match.source]
        target = self.context.target_nodes[match.target]

        assert source.can_match(target)
        assert len(source.children) == len(target.children)

        yield match

        for source_child, target_child in zip(source.children, target.children):
            child_match = MatchingPair(id(source_child), id(target_child))
            yield from self._descendant_matches(child_match)

    def _dice_coefficient(self, match: MatchingPair, compare_parents: bool = False):
        """
        Measures the ratio of common descendants between two nodes.
        """
        source_node = self.context.source_nodes[match.source]
        target_node = self.context.target_nodes[match.target]

        if compare_parents:
            source_node = source_node.parent or source_node
            target_node = target_node.parent or target_node

        cache_key = source_node.metadata.hashcode, target_node.metadata.hashcode
        if cache_key in self.dice_cache:
            return self.dice_cache[cache_key]

        source_descendants = set(id(x) for x in descendants(source_node))
        target_descendants = set(id(x) for x in descendants(target_node))

        common_descendant_matches = sum(
            self.matching_set.source_target_map.get(x) in target_descendants
            for x in source_descendants
        )

        self.dice_cache[cache_key] = (
            2
            * common_descendant_matches
            / (len(source_descendants) + len(target_descendants))
        )

        return self.dice_cache[cache_key]
