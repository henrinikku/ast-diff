import ast
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Tuple

from astdiff.matcher import MatchResult, NodeId


@dataclass(frozen=True)
class Operation:
    node: ast.AST


@dataclass(frozen=True)
class Insert(Operation):
    ...


@dataclass(frozen=True)
class Delete(Operation):
    ...


@dataclass(frozen=True)
class Move(Operation):
    ...


@dataclass(frozen=True)
class Update(Operation):
    ...


EditScript = Tuple[Operation, ...]


class EditScriptGenerator(ABC):
    """
    Base class for all edit script generator implementations.
    Some implementations might for example consider move operations and some might not.
    """

    @abstractmethod
    def generate_edit_script(
        self,
        source_nodes: Dict[NodeId, ast.AST],
        target_nodes: Dict[NodeId, ast.AST],
        result: MatchResult,
    ) -> EditScript:
        ...


class WithMoveEditScriptGenerator(EditScriptGenerator):
    """
    Edit script generator that takes into account move operations.

    Source: Chawathe et al. 1996 https://dl.acm.org/doi/pdf/10.1145/235968.233366
    """

    def generate_edit_script(
        self,
        source_nodes: Dict[NodeId, ast.AST],
        target_nodes: Dict[NodeId, ast.AST],
        result: MatchResult,
    ):
        ops = []

        inserted_ids = set(target_nodes) - result.matched_target_ids
        ops += [Insert(target_nodes[x]) for x in inserted_ids]

        deleted_ids = set(source_nodes) - result.matched_source_ids
        ops += [Delete(source_nodes[x]) for x in deleted_ids]

        # TODO: Generate moves and updates
        return tuple(ops)
