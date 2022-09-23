from dataclasses import dataclass, replace
from functools import cached_property
from typing import Dict, FrozenSet

from astdiff.ast import Node
from astdiff.edit_script import EditScript

NodeId = int


@dataclass(frozen=True)
class MatchingPair:
    source: NodeId
    target: NodeId


MatchingSet = FrozenSet[MatchingPair]


@dataclass
class DiffContext:
    """
    Helper class for holding data that need to be passed along
    between different stages of the algorithm.
    """

    # In data structures that require hashing, nodes are stored and acccessed
    # by their ids in order to avoid recursive hash computations.
    source_nodes: Dict[NodeId, Node]
    target_nodes: Dict[NodeId, Node]

    matching_set: MatchingSet
    edit_script: EditScript

    def copy(self, **changes):
        return replace(self, **changes)

    @cached_property
    def matched_source_ids(self):
        return set(x.source for x in self.matching_set)

    @cached_property
    def matched_target_ids(self):
        return set(x.target for x in self.matching_set)

    @cached_property
    def unmatched_source_ids(self):
        return set(self.source_nodes) - self.matched_source_ids

    @cached_property
    def unmatched_target_ids(self):
        return set(self.target_nodes) - self.matched_target_ids
