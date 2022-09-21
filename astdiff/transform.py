import ast

from astdiff.traversal import post_order_walk


def add_metadata(node: ast.AST):
    AddLabelVisitor().visit(node)
    LeafVisitor().visit(node)
    add_height(node)


def add_field(node: ast.AST, name: str, value):
    """
    Adds a member with given name and value to an AST node.
    """
    setattr(node, name, value)
    if name not in node._fields:
        node._fields += (name,)


def add_height(root: ast.AST):
    """
    Calculates height of each node in given tree.
    """
    for node in post_order_walk(root):
        height = 1 + max([x.height for x in ast.iter_child_nodes(node)] or [0])
        add_field(node, "height", height)


class HashVisitor(ast.NodeVisitor):
    """
    """

    def generic_visit(self, node: ast.AST):
        super().generic_visit(node)

    def hash_leaf(self, node: ast.AST): ...

    def hash_node(self, node: ast.AST, size: int, separator: int):
        return hash(type(node), node.)

class AddLabelVisitor(ast.NodeVisitor):
    """
    Adds a label to the given node and its descendants.
    """

    def generic_visit(self, node: ast.AST):
        label = type(node).__name__
        add_field(node, "label", label)
        super().generic_visit(node)


class LeafVisitor(ast.NodeVisitor):
    """
    Adds is_leaf member to the given node and its descendants.
    """

    def generic_visit(self, node: ast.AST):
        is_leaf = not any(ast.iter_child_nodes(node))
        add_field(node, "is_leaf", is_leaf)
        super().generic_visit(node)
