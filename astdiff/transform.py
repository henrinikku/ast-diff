import ast


def add_field(node: ast.AST, name: str, value):
    """
    Adds a member with given name and value to an AST node.
    """
    setattr(node, name, value)
    if name not in node._fields:
        node._fields += (name,)


class AddLabelVisitor(ast.NodeVisitor):
    """
    Adds a label to the given node and its descendants.
    """

    def generic_visit(self, node: ast.AST):
        label = type(node).__name__
        add_field(node, "label", label)
        super().generic_visit(node)


class CheckLeafVisitor(ast.NodeVisitor):
    """
    Adds is_leaf member to the given node and its descendants.
    """

    def generic_visit(self, node: ast.AST):
        is_leaf = not any(ast.iter_child_nodes(node))
        add_field(node, "is_leaf", is_leaf)
        super().generic_visit(node)


class AddLeafValueVisitor(ast.NodeVisitor):
    """
    Adds a string value to leaves of the given tree.
    """

    def generic_visit(self, node: ast.AST):
        if node.is_leaf:
            value = ast.unparse(node)
            add_field(node, "leaf_value", value)
        super().generic_visit(node)


def add_metadata(node: ast.AST):
    AddLabelVisitor().visit(node)
    CheckLeafVisitor().visit(node)
    AddLeafValueVisitor().visit(node)
