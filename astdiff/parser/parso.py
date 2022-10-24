from typing import List

import parso
from parso.python.tree import EndMarker, Newline, Operator
from parso.tree import NodeOrLeaf as ParsoNode

from astdiff.ast.node import Node, NodePosition
from astdiff.parser.base import Parser


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
