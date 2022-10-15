from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import Tuple

import typic

from astdiff.ast import Node


@typic.al(strict=True)
@dataclass(frozen=True)
class Operation(ABC):
    node: Node

    @abstractmethod
    def apply(self):
        ...

    def standalone(self):
        return replace(self, node=self.node.standalone())


@typic.al(strict=True)
@dataclass(frozen=True)
class Insert(Operation):
    parent: Node
    position: int

    def apply(self):
        children = list(self.parent.children)
        children.insert(self.position, self.node)
        self.parent.children = tuple(children)
        self.node.parent = self.parent

    def standalone(self):
        return replace(
            super().standalone(),
            parent=self.parent.standalone(),
            position=self.position,
        )


@typic.al(strict=True)
@dataclass(frozen=True)
class Move(Insert):
    def apply(self):
        Delete(self.node).apply()
        super().apply()


@typic.al(strict=True)
@dataclass(frozen=True)
class Delete(Operation):
    def apply(self):
        self.node.siblings = tuple(x for x in self.node.siblings if x is not self.node)


@typic.al(strict=True)
@dataclass(frozen=True)
class Update(Operation):
    value: str

    def apply(self):
        self.node.value = self.value

    def standalone(self):
        return replace(super().standalone(), value=self.value)


class EditScript(Tuple[Operation, ...]):
    def standalone(self):
        return EditScript(op.standalone() for op in self)
