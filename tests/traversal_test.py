import ast
import unittest

from astdiff.traversal import post_order_walk, pre_order_walk


class TraversalTest(unittest.TestCase):
    def setUp(self):
        self.ast = ast.parse("print('foo')")

    def test_post_order_walk(self):
        node_types = [type(x) for x in post_order_walk(self.ast)]

        self.assertEqual(
            node_types,
            [
                ast.Load,
                ast.Name,
                ast.Constant,
                ast.Call,
                ast.Expr,
                ast.Module,
            ],
        )

    def test_pre_order_walk(self):
        node_types = [type(x) for x in pre_order_walk(self.ast)]

        self.assertEqual(
            node_types,
            [
                ast.Module,
                ast.Expr,
                ast.Call,
                ast.Name,
                ast.Load,
                ast.Constant,
            ],
        )
