import ast
import unittest
from astdiff.change_distilling import ChangeDistilling
from astdiff.io import read_ast


class ChangeDistillingTest(unittest.TestCase):
    def setUp(self):
        source_ast = ast.parse("print('123')")
        target_ast = ast.parse("print('123')")
        self.change_distilling = ChangeDistilling(source_ast, target_ast)

    def test_diff(self):
        assert self.change_distilling.diff() is None
