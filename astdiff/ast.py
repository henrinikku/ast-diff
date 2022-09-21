from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import parso
from parso.python.tree import EndMarker, Newline, Operator
from parso.tree import NodeOrLeaf

_REDUNDANT_PARSO_NODES = (
    Newline,
    EndMarker,
)
_REDUNDANT_PARSO_OPERATORS = (
    ".",
    ":",
    ";",
    "(",
    ")",
    "[",
    "]",
    "",
)


def _redundant(node: NodeOrLeaf):
    if isinstance(node, _REDUNDANT_PARSO_NODES):
        return True

    if isinstance(node, Operator) and node.value in _REDUNDANT_PARSO_OPERATORS:
        return True

    return False


def parse(file_path: str):
    file_text = Path(file_path).read_text()
    return Node.from_code(file_text)


@dataclass(frozen=True)
class Node:
    label: str
    value: str
    children: Tuple["Node", ...]

    @property
    def is_leaf(self):
        return not self.children

    @classmethod
    def from_code(cls, code: str):
        parso_node = parso.parse(code)
        return cls.from_parso_node(parso_node)

    @classmethod
    def from_parso_node(cls, node: NodeOrLeaf):
        value = getattr(node, "value", "")
        children = getattr(node, "children", [])
        return cls(
            label=node.type,
            value=value,
            children=tuple(
                cls.from_parso_node(x) for x in children if not _redundant(x)
            ),
        )


@dataclass(frozen=True)
class NodeMetadata:
    hash: int
