from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Optional

import typic

from astdiff.ast.node import Node


@typic.al(strict=True)
@dataclass(frozen=True)
class Operation(ABC):
    """
    Base class for all edit operations.
    """

    node: Node

    @abstractmethod
    def apply(self):
        """
        Applies the operation to the source tree.
        """
        ...

    def standalone(self):
        """
        Returns a copy of self with references to standalone nodes.
        """
        return replace(self, node=self.node.standalone())


@typic.al(strict=True)
@dataclass(frozen=True)
class Insert(Operation):
    """
    Represents an insert operation.
    """

    parent: Optional[Node]
    position: int

    def apply(self):
        """
        Inserts node to the specified parent.
        """
        if self.parent is None:
            return
        children = list(self.parent.children)
        children.insert(self.position, self.node)
        self.parent.children = tuple(children)
        self.node.parent = self.parent

    def standalone(self):
        return replace(super().standalone(), parent=self.parent.standalone())


@typic.al(strict=True)
@dataclass(frozen=True)
class Move(Insert):
    """
    Represents a move operation.
    """

    def apply(self):
        """
        Moves a node to the specified parent.
        """
        Delete(self.node).apply()
        super().apply()


@typic.al(strict=True)
@dataclass(frozen=True)
class Delete(Operation):
    """
    Represents a delete operation.
    """

    def apply(self):
        """
        Deletes a node from the tree.
        """
        self.node.siblings = tuple(x for x in self.node.siblings if x is not self.node)


@typic.al(strict=True)
@dataclass(frozen=True)
class Update(Operation):
    """
    Represents an update operation.
    """

    value: str
    old_value: Optional[str] = field(default=None, repr=False, compare=False)

    def apply(self):
        """
        Updates the value of a node.
        """
        self.node.value = self.value

    def standalone(self):
        return replace(
            self,
            node=replace(self.node.standalone(), value=self.old_value or self.value),
        )
