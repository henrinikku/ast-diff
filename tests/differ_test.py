import parso
import unittest
from astdiff.differ import diff
from astdiff.util import read_ast


class DifferTest(unittest.TestCase):
    def test_diff(self):
        source_ast = parso.parse("print('123')")
        target_ast = parso.parse("print('321')")
        edit_script = diff(source_ast, target_ast)
        self.assertIsNotNone(edit_script)
