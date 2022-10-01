from dataclasses import dataclass, field, replace
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
    position: int = 0


@total_ordering
@dataclass
class Node:
    label: str
    value: str
    children: Tuple["Node", ...] = field(default_factory=tuple, repr=False)
    parent: Optional["Node"] = field(default=None, repr=False, compare=False)
    metadata: Optional[NodeMetadata] = field(default=None, repr=False)

    @property
    def is_leaf(self):
        return not self.children

    @property
    def is_root(self):
        return not self.parent

    def standalone(self):
        return replace(self, children=(), parent=None, metadata=None)

    def can_match(self, other: "Node"):
        return (self.label, self.is_root) == (other.label, other.is_root)

    def isomorphic_to(self, other: "Node"):
        """
        Checks if self is isomorphic to given tree.
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
