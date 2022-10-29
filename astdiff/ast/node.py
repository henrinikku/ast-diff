from dataclasses import dataclass, field, replace
from functools import total_ordering
from typing import Optional, Tuple


@dataclass(frozen=True)
class NodeMetadata:
    """
    Helper class for holding metadata that is calculated for each node after parsing.
    """

    hashcode: int
    """
    Trees have the same hashcode iff they are isomorphic.
    Note that labels and values are taken into account when computing hashcodes.
    """

    height: int
    size: int


@dataclass(frozen=True)
class NodePosition:
    """
    Represents the start and end positions of a node in the code file.
    """

    start_line: int
    start_col: int
    end_line: int
    end_col: int


@total_ordering
@dataclass
class Node:
    """
    Represents a node in an AST.
    """

    label: str
    value: str
    children: Tuple["Node", ...] = field(default_factory=tuple, repr=False)
    parent: Optional["Node"] = field(default=None, repr=False, compare=False)
    metadata: Optional[NodeMetadata] = field(default=None, repr=False, compare=False)
    position: Optional[NodePosition] = field(default=None, repr=False, compare=False)

    @property
    def is_leaf(self):
        return not self.children

    @property
    def is_root(self):
        return self.parent is None

    @property
    def position_in_siblings(self):
        return next(
            (i for i, sibling in enumerate(self.siblings) if self is sibling), None
        )

    @property
    def siblings(self):
        return (self.parent and self.parent.children) or ()

    @siblings.setter
    def siblings(self, value: Tuple["Node", ...]):
        if self.parent:
            self.parent.children = value

    @property
    def compare_fields(self):
        """
        Fields used for comparing nodes. The exact ordering of nodes is not important
        but it must be stable / deterministic.
        """
        hashcode = (self.metadata and (self.metadata.hashcode,)) or ()
        return (self.label, self.value, len(self.children)) + hashcode

    def standalone(self):
        """
        Returns a copy of self without references to other nodes. Used simplify testing.
        """
        return replace(self, children=(), parent=None, metadata=None)

    def can_match(self, other: "Node"):
        """
        Defines the minimum criteria for forming a match between two nodes.
        """
        return self.label == other.label

    def isomorphic_to(self, other: "Node"):
        """
        Checks if self is isomorphic to given tree using pre-calculated hashcodes.
        """
        return (
            self.metadata
            and other.metadata
            and self.metadata.hashcode == other.metadata.hashcode
        )

    def isomorphic_to_without_values(self, other: "Node"):
        """
        Checks if self is isomporphic to given tree when node values are ignored.
        Runs in linear time when 'self' and 'other' are isomorphic without values.
        """
        return (
            self
            and other
            and self.can_match(other)
            and len(self.children) == len(other.children)
            and all(
                a.isomorphic_to_without_values(b)
                for a, b in zip(self.children, other.children)
            )
        )

    def __lt__(self, other: "Node"):
        return self.compare_fields < other.compare_fields
