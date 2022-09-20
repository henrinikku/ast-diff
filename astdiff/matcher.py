import ast
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Set

logger = logging.getLogger(__name__)

NodeId = int


@dataclass(frozen=True)
class MatchingPair:
    source: NodeId
    target: NodeId


@dataclass(frozen=True)
class MatchResult:
    matched_ids: Set[MatchingPair]

    @cached_property
    def matched_source_ids(self):
        return set(x.source for x in self.matched_ids)

    @cached_property
    def matched_target_ids(self):
        return set(x.target for x in self.matched_ids)


class Matcher(ABC):
    @abstractmethod
    def find_matching_nodes(self, source: ast.AST, target: ast.AST) -> MatchResult:
        ...


class StubMatcher(Matcher):
    def find_matching_nodes(self, source: ast.AST, target: ast.AST):
        return MatchResult(set())


class ChangeDistillingMatcher(Matcher):
    def find_matching_nodes(self, source: ast.AST, target: ast.AST):
        raise NotImplementedError()
