import ast
import unittest

from astdiff.util import read_ast
from astdiff.transform import add_metadata, add_field, add_height


class TransformTest(unittest.TestCase):
    def setUp(self):
        self.ast = read_ast("tests/data/test2.py")

    def test_add_field_adds_field(self):
        root = self.ast
        add_field(root, "foo", "bar")

        assert hasattr(root, "foo")
        assert "foo" in root._fields
        assert root.foo == "bar"

    def test_add_field_is_idempotent(self):
        root = self.ast
        add_field(root, "foo", "bar")

        fields_total = len(root._fields)
        for __ in range(10):
            add_field(root, "foo", "bar")

        assert len(root._fields) == fields_total

    def test_add_metadata_adds_label(self):
        add_metadata(self.ast)

        assert all(hasattr(x, "label") for x in ast.walk(self.ast))
        assert all("label" in x._fields for x in ast.walk(self.ast))

    def test_add_metadata_adds_is_leaf(self):
        add_metadata(self.ast)

        assert all(hasattr(x, "is_leaf") for x in ast.walk(self.ast))
        assert all("is_leaf" in x._fields for x in ast.walk(self.ast))

    def test_add_height(self):
        root = ast.parse("print('123')")
        add_height(root)
        assert root.height == 5

        root = ast.parse("'123'")
        add_height(root)
        assert root.height == 3

        add_metadata(root)
        assert all(x.height == 1 for x in ast.walk(root) if x.is_leaf)
