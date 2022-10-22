import ast
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, List, Optional, TypeVar, final

import parso
from parso.python.tree import EndMarker, Newline, Operator
from parso.tree import NodeOrLeaf as ParsoNode

from astdiff.ast.metadata import add_parents, attach_metadata
from astdiff.ast.node import Node, NodePosition


@dataclass(frozen=True)
class ParseOptions:
    add_metadata: bool = True
    add_parent: bool = False


T = TypeVar("T")


class Parser(ABC, Generic[T]):
    """
    Base class for parser implementations.
    Inheriting classes implement parsing using different libraries (e.g. parso, ast).

    Inputs:
        T: Generic node type provided by the parsing library.
    """

    def __init__(self, options: Optional[ParseOptions] = None):
        self.options = options or ParseOptions()

    @final
    def parse(self, input: str) -> Node:
        return (
            self.parse_file(input) if input.endswith(".py") else self.parse_code(input)
        )

    @final
    def parse_file(self, file_path: str) -> Node:
        code = Path(file_path).read_text()
        return self.parse_code(code)

    @final
    def parse_code(self, code: str) -> Node:
        tree = self.parse_with_lib(code)
        canonical_tree = self.canonicalize(tree)

        if self.options.add_metadata:
            attach_metadata(canonical_tree)

        if self.options.add_parent:
            add_parents(canonical_tree)

        return canonical_tree

    @abstractmethod
    def parse_with_lib(self, code: str) -> T:
        ...

    @abstractmethod
    def canonicalize(self, node: T) -> Node:
        ...


class BuiltInASTParser(Parser[ast.AST]):
    """
    Parser implementation based on Python's built-in 'ast' library.
    """

    def parse_with_lib(self, code: str) -> ast.AST:
        return ast.parse(code)

    def canonicalize(self, node: ast.AST):
        label = type(node).__name__
        value = self._get_value(node)
        position = NodePosition(
            node.lineno, node.col_offset, node.end_lineno, node.end_col_offset
        )
        children = tuple(self.canonicalize(x) for x in ast.iter_child_nodes(node))
        return Node(label, value, position=position, children=children)

    def _get_value(self, node: ast.AST):
        pass


class ParsoParser(Parser[ParsoNode]):
    """
    Parser implementation based on 'parso' library.
    """

    _REDUNDANT_NODES = (
        Newline,
        EndMarker,
    )
    _REDUNDANT_OPERATORS = (
        "",
        ".",
        ":",
        ";",
        "(",
        ")",
        "[",
        "]",
    )

    def parse_with_lib(self, code: str) -> ParsoNode:
        return parso.parse(code)

    def canonicalize(self, node: ParsoNode):
        label = node.type
        value = getattr(node, "value", "")
        position = NodePosition(*node.start_pos, *node.end_pos)
        children = tuple(
            self.canonicalize(x)
            for x in self._iter_child_nodes(node)
            if not self._redundant(x)
        )
        return Node(label, value, position=position, children=children)

    @classmethod
    def _iter_child_nodes(cls, node: ParsoNode):
        children: List[ParsoNode] = getattr(node, "children", [])
        for child in children:
            if child.type == "atom":
                yield from cls._iter_child_nodes(child)
            else:
                yield child

    @classmethod
    def _redundant(cls, node: ParsoNode):
        if isinstance(node, cls._REDUNDANT_NODES):
            return True

        if isinstance(node, Operator) and node.value in cls._REDUNDANT_OPERATORS:
            return True

        return False
