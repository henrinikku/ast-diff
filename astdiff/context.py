from dataclasses import dataclass, field, replace
from functools import total_ordering
from typing import Dict, Iterable

from astdiff.ast import Node
from astdiff.edit_script import EditScript

NodeId = int


@total_ordering
@dataclass(frozen=True)
class MatchingPair:
    source: NodeId
    target: NodeId

    def __lt__(self, other: "MatchingPair"):
        return (self.source, self.target) < (other.source, other.target)


@dataclass(frozen=True)
class MatchingSet:
    source_target_map: Dict[NodeId, NodeId] = field(default_factory=dict)
    target_source_map: Dict[NodeId, NodeId] = field(default_factory=dict)

    def add(self, pair: MatchingPair):
        assert not self.matched(pair)

        self.source_target_map[pair.source] = pair.target
        self.target_source_map[pair.target] = pair.source

    def update(self, pairs: Iterable[MatchingPair]):
        for pair in pairs:
            self.add(pair)

    def matched(self, pair: MatchingPair):
        return (
            pair.source in self.source_target_map
            or pair.target in self.target_source_map
        )

    def __len__(self):
        assert len(self.source_target_map) == len(self.target_source_map)
        return len(self.source_target_map)

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

    matching_set: MatchingSet = field(default_factory=MatchingSet)
    edit_script: EditScript = field(default_factory=tuple)

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
