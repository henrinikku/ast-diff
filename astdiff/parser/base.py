from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Optional, TypeVar, final

from astdiff.ast.metadata import add_parents, attach_metadata
from astdiff.ast.node import Node


@dataclass(frozen=True)
class ParseOptions:
    add_metadata: bool = True
    add_parent: bool = False


T = TypeVar("T")


class Parser(ABC, Generic[T]):
    """
    Base class for parser implementations.
    Inheriting classes implement parsing using different libraries (e.g. parso, ast).

    Inputs:
        T: Generic node type provided by the parsing library.
    """

    def __init__(self, options: Optional[ParseOptions] = None):
        self.options = options or ParseOptions()

    @final
    def parse(self, input: str) -> Node:
        """
        Parses the input (python code or path to a python file) and
        returns the resulting AST.
        """
        return (
            self.parse_file(input) if input.endswith(".py") else self.parse_code(input)
        )

    @final
    def parse_file(self, file_path: str) -> Node:
        """
        Parses the given source file and returns the resulting AST.
        """
        code = Path(file_path).read_text()
        return self.parse_code(code)

    @final
    def parse_code(self, code: str) -> Node:
        """
        Parses the given code and returns the resulting AST.
        """
        tree = self.parse_with_lib(code)
        canonical_tree = self.canonicalize(tree)

        if self.options.add_metadata:
            attach_metadata(canonical_tree)

        if self.options.add_parent:
            add_parents(canonical_tree)

        return canonical_tree

    @abstractmethod
    def parse_with_lib(self, code: str) -> T:
        """
        Parses the code using an external library.
        """
        ...

    @abstractmethod
    def canonicalize(self, node: T) -> Node:
        """
        Normalizes the AST returned by an external library to the format
        used internally by this program.
        """
        ...
