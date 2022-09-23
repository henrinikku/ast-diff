from dataclasses import dataclass, replace
from functools import total_ordering
from typing import Optional, Tuple


@dataclass(frozen=True)
class NodeMetadata:
    hashcode: int
    """
    Trees have the same hashcode iff they are isomorphic.
    Note that labels and values are taken into account when computing hashcodes.
    """

    height: int
    size: int


@total_ordering
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
        """
        Checks if self is isomorphic to the given tree.
        """
        return (
            self.metadata
            and other.metadata
            and self.metadata.hashcode == other.metadata.hashcode
        )

    def __lt__(self, other: "Node"):
        return (self.label, self.value, len(self.children)) < (
            other.label,
            other.value,
            len(other.children),
        )
