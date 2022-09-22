from pathlib import Path
from typing import List

import parso
from parso.python.tree import EndMarker, Newline, Operator
from parso.tree import NodeOrLeaf as ParsoNode

from astdiff.ast import Node
from astdiff.metadata import attach_metadata
from astdiff.traversal import post_order_walk


def parse(file_path: str, add_metadata: bool = True):
    file_text = Path(file_path).read_text()
    return parse_code(file_text, add_metadata)


def parse_code(code: str, add_metadata: bool = True):
    parso_tree = parso.parse(code)
    canonical_tree = canonicalize(parso_tree)
    if add_metadata:
        attach_metadata(canonical_tree)
    return canonical_tree


def canonicalize(node: ParsoNode):
    label = node.type
    value = getattr(node, "value", "")
    children = tuple(
        canonicalize(x) for x in _iter_child_nodes(node) if not _redundant(x)
    )
    return Node(label, value, children)


_REDUNDANT_PARSO_NODES = (
    Newline,
    EndMarker,
)
_REDUNDANT_PARSO_OPERATORS = (
    "",
    ".",
    ":",
    ";",
    "(",
    ")",
    "[",
    "]",
)


def _iter_child_nodes(node: ParsoNode):
    children: List[ParsoNode] = getattr(node, "children", [])
    for child in children:
        if child.type == "atom":
            yield from _iter_child_nodes(child)
        else:
            yield child


def _redundant(node: ParsoNode):
    if isinstance(node, _REDUNDANT_PARSO_NODES):
        return True

    if isinstance(node, Operator) and node.value in _REDUNDANT_PARSO_OPERATORS:
        return True

    return False
