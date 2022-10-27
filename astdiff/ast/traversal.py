from collections import deque

from astdiff.ast.node import Node


def descendants(node: Node):
    """
    Yields descendants of the given node in pre-order.
    """
    descendant_nodes = pre_order_walk(node)
    next(descendant_nodes)
    yield from descendant_nodes


def pre_order_walk(node: Node):
    """
    Yields nodes of given tree in pre-order, i.e.,
    can be used for top-down traversal.
    """
    yield node

    for child in node.children:
        yield from pre_order_walk(child)


def post_order_walk(node: Node):
    """
    Yields nodes of the given tree in post-order, i.e.,
    can be used for bottom-up traversal.
    """
    for child in node.children:
        yield from post_order_walk(child)

    yield node


def bfs(tree: Node):
    """
    Yields nodes from the breadth-first traversal of the given tree.
    """
    queue = deque([tree])
    while queue:
        node = queue.popleft()
        queue.extend(node.children)
        yield node
