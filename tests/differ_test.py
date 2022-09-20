import ast
import unittest
from astdiff.differ import diff
from astdiff.io import read_ast


class ChangeDistillingTest(unittest.TestCase):
    def test_diff(self):
        source_ast = ast.parse("print('123')")
        target_ast = ast.parse("print('123')")
        assert diff(source_ast, target_ast)
