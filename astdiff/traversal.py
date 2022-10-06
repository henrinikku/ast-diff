from collections import deque

from astdiff.ast import Node


def descendants(node: Node):
    descendant_nodes = pre_order_walk(node)
    next(descendant_nodes)
    yield from descendant_nodes


def pre_order_walk(node: Node):
    yield node

    for child in node.children:
        yield from pre_order_walk(child)


def post_order_walk(node: Node):
    for child in node.children:
        yield from post_order_walk(child)

    yield node


def bfs(tree: Node):
    queue = deque([tree])
    while queue:
        node = queue.popleft()
        queue.extend(node.children)
        yield node
