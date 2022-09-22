from dataclasses import dataclass, replace
from typing import Optional, Tuple


@dataclass(frozen=True)
class NodeMetadata:
    hashcode: int
    height: int
    size: int


@dataclass
class Node:
    label: str
    value: str
    children: Tuple["Node", ...]
    metadata: Optional[NodeMetadata] = None

    @property
    def is_leaf(self):
        return not self.children

    def standalone(self):
        return replace(self, children=(), metadata=None)

    def isomorphic_to(self, other: "Node"):
        return (
            self.metadata
            and other.metadata
            and self.metadata.hashcode == other.metadata.hashcode
        )
