import ast


def pre_order_walk(node: ast.AST):
    yield node

    for child in ast.iter_child_nodes(node):
        yield from pre_order_walk(child)


def post_order_walk(node: ast.AST):
    for child in ast.iter_child_nodes(node):
        yield from post_order_walk(child)

    yield node
