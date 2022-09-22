import unittest

from astdiff.differ import diff
from astdiff.parse import parse_code


class DifferTest(unittest.TestCase):
    def test_diff(self):
        source_ast = parse_code("print('123')")
        target_ast = parse_code("print('321')")
        edit_script = diff(source_ast, target_ast)

        assert bool(edit_script)
