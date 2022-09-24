from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import parso
from parso.python.tree import EndMarker, Newline, Operator
from parso.tree import NodeOrLeaf as ParsoNode

from astdiff.ast import Node
from astdiff.metadata import attach_metadata


@dataclass(frozen=True)
class ParseOptions:
    add_metadata: bool = True
    add_parent: bool = False


def parse(file_path: str, options: ParseOptions = ParseOptions()):
    file_text = Path(file_path).read_text()
    return parse_code(file_text, options)


def parse_code(code: str, options: ParseOptions = ParseOptions()):
    parso_tree = parso.parse(code)
    canonical_tree = canonicalize(parso_tree)
    if options.add_metadata:
        attach_metadata(canonical_tree)
    return canonical_tree


def canonicalize(
    node: ParsoNode,
    options: ParseOptions = ParseOptions(),
    parent: Optional[Node] = None,
):
    label = node.type
    value = getattr(node, "value", "")

    canonical_node = Node(label, value, parent=parent, children=())
    parent_node = canonical_node if options.add_parent else None

    canonical_node.children = tuple(
        canonicalize(x, options, parent_node)
        for x in _iter_child_nodes(node)
        if not _redundant(x)
    )

    return canonical_node


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
