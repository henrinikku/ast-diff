from astdiff.ast import Node


def pre_order_walk(node: Node):
    yield node

    for child in node.children:
        yield from pre_order_walk(child)


def post_order_walk(node: Node):
    for child in node.children:
        yield from post_order_walk(child)

    yield node
