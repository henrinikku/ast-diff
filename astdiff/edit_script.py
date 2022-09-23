from dataclasses import dataclass
from typing import Tuple

from astdiff.ast import Node


@dataclass(frozen=True)
class Operation:
    node: Node


@dataclass(frozen=True)
class Insert(Operation):
    ...


@dataclass(frozen=True)
class Delete(Operation):
    ...


@dataclass(frozen=True)
class Move(Operation):
    ...


@dataclass(frozen=True)
class Update(Operation):
    ...


EditScript = Tuple[Operation, ...]
