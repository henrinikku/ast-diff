import ast
import unittest

import parso
import parso.python.tree
import parso.tree

from astdiff.ast.node import Node
from astdiff.ast.parser import BuiltInASTParser, ParseOptions, ParsoParser


class ParsoParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = ParsoParser(ParseOptions(add_metadata=False))

    def test_parse(self):
        ast = self.parser.parse_file("tests/data/print_123.py")

        assert ast == Node(
            label="file_input",
            value="",
            children=(
                Node(
                    label="simple_stmt",
                    value="",
                    children=(
                        Node(
                            label="atom_expr",
                            value="",
                            children=(
                                Node(label="name", value="print", children=()),
                                Node(
                                    label="trailer",
                                    value="",
                                    children=(
                                        Node(
                                            label="string", value='"123"', children=()
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )

    def test_parsing_ignores_whitespace(self):
        with_whitespace = self.parser.parse_code("print(        'foo')")
        without_whitespace = self.parser.parse_code("print('foo')")
        assert with_whitespace == without_whitespace

    def test_parsing_ignores_parens(self):
        with_parens = self.parser.parse_code("a = (((((((1)))))))")
        without_parens = self.parser.parse_code("a = 1")
        assert with_parens == without_parens

    def test_create_from_parso_ast(self):
        parso_ast = parso.parse("if True == True: print('foo')")
        canonical = self.parser.canonicalize(parso_ast)
        assert canonical == Node(
            label="file_input",
            value="",
            children=(
                Node(
                    label="if_stmt",
                    value="",
                    children=(
                        Node(label="keyword", value="if", children=()),
                        Node(
                            label="comparison",
                            value="",
                            children=(
                                Node(label="keyword", value="True", children=()),
                                Node(label="operator", value="==", children=()),
                                Node(label="keyword", value="True", children=()),
                            ),
                        ),
                        Node(
                            label="atom_expr",
                            value="",
                            children=(
                                Node(label="name", value="print", children=()),
                                Node(
                                    label="trailer",
                                    value="",
                                    children=(
                                        Node(
                                            label="string", value="'foo'", children=()
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )


class BuiltInASTParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = BuiltInASTParser(ParseOptions(add_metadata=False))

    def test_parse(self):
        ast = self.parser.parse_file("tests/data/print_123.py")
        assert ast == Node(
            label="Module",
            value=None,
            children=(
                Node(
                    label="Expr",
                    value=None,
                    children=(
                        Node(
                            label="Call",
                            value=None,
                            children=(
                                Node(
                                    label="Name",
                                    value="print",
                                    children=(
                                        Node(label="Load", value=None, children=()),
                                    ),
                                ),
                                Node(label="Constant", value="123", children=()),
                            ),
                        ),
                    ),
                ),
            ),
        )

    def test_parsing_ignores_whitespace(self):
        with_whitespace = self.parser.parse_code("print(        'foo')")
        without_whitespace = self.parser.parse_code("print('foo')")
        assert with_whitespace == without_whitespace

    def test_parsing_ignores_parens(self):
        with_parens = self.parser.parse_code("a = (((((((1)))))))")
        without_parens = self.parser.parse_code("a = 1")
        assert with_parens == without_parens

    def test_create_from_builtin_ast(self):
        builtin_ast = ast.parse("if True == True: print('foo')")
        canonical = self.parser.canonicalize(builtin_ast)
        assert canonical == Node(
            label="Module",
            value=None,
            children=(
                Node(
                    label="If",
                    value=None,
                    children=(
                        Node(
                            label="Compare",
                            value=None,
                            children=(
                                Node(label="Constant", value=True, children=()),
                                Node(label="Eq", value=None, children=()),
                                Node(label="Constant", value=True, children=()),
                            ),
                        ),
                        Node(
                            label="Expr",
                            value=None,
                            children=(
                                Node(
                                    label="Call",
                                    value=None,
                                    children=(
                                        Node(
                                            label="Name",
                                            value="print",
                                            children=(
                                                Node(
                                                    label="Load",
                                                    value=None,
                                                    children=(),
                                                ),
                                            ),
                                        ),
                                        Node(
                                            label="Constant", value="foo", children=()
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )
