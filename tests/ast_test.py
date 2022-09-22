import unittest

import parso
import parso.tree
import parso.python.tree

from astdiff.ast import Node, parse


class ASTTest(unittest.TestCase):
    def test_parse(self):
        ast = parse("tests/data/print_123.py")
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
        with_whitespace = Node.from_code("print(        'foo'")
        without_whitespace = Node.from_code("print('foo'")
        assert with_whitespace == without_whitespace

    def test_parsing_ignores_whitespace(self):
        with_parens = Node.from_code("a = (((((((1)))))))")
        without_parens = Node.from_code("a = 1")
        assert with_parens == without_parens

    def test_create_from_parso_ast(self):
        parso_ast = parso.parse("if True == True: print('foo')")
        canonical = Node.from_parso_node(parso_ast)

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
