import unittest

from astdiff.differ import diff
from astdiff.parse import ParsoParser


class DifferTest(unittest.TestCase):
    def test_diff(self):
        parser = ParsoParser()
        source_ast = parser.parse_code("print('123')")
        target_ast = parser.parse_code("print('321')")
        edit_script = diff(source_ast, target_ast)

        assert bool(edit_script)
