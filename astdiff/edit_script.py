from abc import ABC
from dataclasses import dataclass
from typing import Tuple

from astdiff.ast import Node


class Operation(ABC):
    ...


@dataclass(frozen=True)
class Insert(Operation):
    node: Node


@dataclass(frozen=True)
class Delete(Operation):
    node: Node


@dataclass(frozen=True)
class Move(Operation):
    node: Node
    source_parent: Node
    target_parent: Node


@dataclass(frozen=True)
class Update(Operation):
    source: Node
    target: Node


EditScript = Tuple[Operation, ...]
