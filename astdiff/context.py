from dataclasses import dataclass, replace
from typing import Dict, Iterable

from astdiff.ast import Node
from astdiff.edit_script import EditScript

NodeId = int


@dataclass(frozen=True)
class MatchingPair:
    source: NodeId
    target: NodeId


@dataclass
class MatchingSet:
    source_target_map: Dict[NodeId, NodeId]
    target_source_map: Dict[NodeId, NodeId]

    def __init__(self):
        self.source_target_map = {}
        self.target_source_map = {}

    def add(self, pair: MatchingPair):
        assert self.unmatched(pair)

        self.source_target_map[pair.source] = pair.target
        self.target_source_map[pair.target] = pair.source

    def update(self, pairs: Iterable[MatchingPair]):
        for pair in pairs:
            self.add(pair)

    def unmatched(self, pair: MatchingPair):
        return (
            pair.source not in self.source_target_map
            and pair.target not in self.target_source_map
        )

    @property
    def pairs(self):
        return (MatchingPair(s, t) for s, t in self.source_target_map.items())


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

    @property
    def matched_source_ids(self):
        return set(self.matching_set.source_target_map)

    @property
    def matched_target_ids(self):
        return set(self.matching_set.target_source_map)

    @property
    def unmatched_source_ids(self):
        return set(self.source_nodes) - self.matched_source_ids

    @property
    def unmatched_target_ids(self):
        return set(self.target_nodes) - self.matched_target_ids
