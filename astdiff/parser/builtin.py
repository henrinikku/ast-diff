import ast

from astdiff.ast.node import Node, NodePosition
from astdiff.parser.base import Parser


class BuiltInASTParser(Parser[ast.AST]):
    """
    Parser implementation based on Python's built-in 'ast' library.
    """

    _POSSIBLE_VALUE_FIELDS = (
        "value",
        "name",
        "id",
        "n",
        "s",
        "arg",
        "module",
    )
    _PRIMITIVE_TYPES = (
        int,
        float,
        bool,
        str,
    )
    _MISSING = object()

    def parse_with_lib(self, code: str) -> ast.AST:
        return ast.parse(code)

    def canonicalize(self, node: ast.AST):
        label = type(node).__name__
        value = self._get_value(node)
        has_position_info = hasattr(node, "lineno")
        position = (
            NodePosition(
                node.lineno, node.col_offset, node.end_lineno, node.end_col_offset
            )
            if has_position_info
            else None
        )
        children = tuple(self.canonicalize(x) for x in ast.iter_child_nodes(node))
        return Node(label, value, position=position, children=children)

    @classmethod
    def _get_value(cls, node: ast.AST):
        for fieldname in cls._POSSIBLE_VALUE_FIELDS:
            value = getattr(node, fieldname, cls._MISSING)
            if value is not cls._MISSING and isinstance(value, cls._PRIMITIVE_TYPES):
                return str(value)

        return ""
