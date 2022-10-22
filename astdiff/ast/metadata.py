from astdiff.ast.node import Node, NodeMetadata
from astdiff.ast.traversal import post_order_walk

_HASH_START = "start"
_HASH_END = "end"
_HASH_BASE = 33


def add_parents(tree: Node):
    for node in post_order_walk(tree):
        for child in node.children:
            child.parent = node


def attach_metadata(tree: Node):
    """
    Walks given tree via bottom-up recursion and attaches metadata
    to each node based on child results.
    """
    for node in post_order_walk(tree):
        node.metadata = NodeMetadata(
            size=_calculate_size(node),
            height=_calculate_height(node),
            hashcode=_calculate_hash(node),
        )


def _calculate_size(node: Node):
    if node.is_leaf:
        return 1

    return 1 + sum(x.metadata.size for x in node.children)


def _calculate_height(node: Node):
    if node.is_leaf:
        return 1

    return 1 + max(x.metadata.height for x in node.children)


def _calculate_hash(node: Node):
    if node.is_leaf:
        return _hash_node(node, mid_hash=0, exponent=1)

    current_hash = 0
    current_size = 0

    def exponent():
        return 2 * current_size + 1

    for child in node.children:
        current_hash += child.metadata.hashcode * _factor(exponent())
        current_size += child.metadata.size

    return _hash_node(node, mid_hash=current_hash, exponent=exponent())


def _hash_node(node: Node, mid_hash: int, exponent: int):
    return sum(
        (
            hash((node.label, node.value, _HASH_START)),
            mid_hash,
            hash((node.label, node.value, _HASH_END)) * _factor(exponent),
        )
    )


def _factor(num: int):
    return _HASH_BASE**num
