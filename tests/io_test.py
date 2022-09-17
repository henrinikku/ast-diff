import ast

from astdiff.io import read_ast


def test_read_ast():
    expected = ast.parse("print('123')")
    actual = read_ast("tests/data/print_123.py")
    assert ast.dump(expected) == ast.dump(actual)
