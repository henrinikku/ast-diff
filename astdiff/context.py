import ast
from dataclasses import dataclass, replace
from functools import cached_property
from typing import Dict, FrozenSet, Optional

NodeId = int


@dataclass(frozen=True)
class MatchingPair:
    source: NodeId
    target: NodeId


MatchingSet = FrozenSet[MatchingPair]


@dataclass(frozen=True)
class DiffContext:
    """
    Helper class for holding data that need to be passed along
    between different stages of the algorithm.
    """

    # During computation nodes are stored, moved around, and accessed by their ids
    # because Python ASTs are not hashable by default.
    source_nodes: Dict[NodeId, ast.AST]
    target_nodes: Dict[NodeId, ast.AST]
    matching_set: MatchingSet

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
