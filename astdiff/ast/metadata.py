from astdiff.ast.node import Node, NodeMetadata
from astdiff.ast.traversal import post_order_walk


def add_parents(tree: Node):
    """
    Adds a references to parents of each node in the given tree.
    """
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
    """
    Calculates size of the given node, assuming that it has already been
    calculated for its children.
    """
    if node.is_leaf:
        return 1

    return 1 + sum(x.metadata.size for x in node.children)


def _calculate_height(node: Node):
    """
    Calculates height of the given node, assuming that it has already been
    calculated for its children.
    """
    if node.is_leaf:
        return 1

    return 1 + max(x.metadata.height for x in node.children)


_HASH_START = "HASH_START"
_HASH_END = "HASH_END"
_HASH_BASE = 33


def _calculate_hash(node: Node):
    """
    Calculates a hashcode for the given node. Hashcodes are calculated
    such that only identical ASTs share the same hashcode.

    Exact details of the algorithm are not given in the paper, so the implementation
    is adapted from the one used by https://github.com/GumTreeDiff/gumtree.

    Source: Chilowicz et al. 2009
    https://igm.univ-mlv.fr/~chilowi/research/syntax_tree_fingerprinting/syntax_tree_fingerprinting_ICPC09.pdf
    """
    if node.is_leaf:
        return _hash_node(node, current_hash=0, exponent=1)

    current_hash = 0
    current_size = 0

    def exponent():
        return 2 * current_size + 1

    for child in node.children:
        current_hash += child.metadata.hashcode * _factor(exponent())
        current_size += child.metadata.size

    return _hash_node(node, current_hash=current_hash, exponent=exponent())


def _hash_node(node: Node, current_hash: int, exponent: int):
    return sum(
        (
            hash((node.label, node.value, _HASH_START)),
            current_hash,
            hash((node.label, node.value, _HASH_END)) * _factor(exponent),
        )
    )


def _factor(num: int):
    return _HASH_BASE**num
