import unittest

from astdiff.ast import Node
from astdiff.parse import parse, parse_code
from astdiff.metadata import attach_metadata


class MetadataTest(unittest.TestCase):
    def test_size_calculation_parsed_tree(self):
        tree = parse_code("print(1)")
        assert tree.metadata.size == 5

    def test_size_calculation_empty_tree(self):
        tree = Node("test", "", tuple())
        attach_metadata(tree)
        assert tree.metadata.size == 1

    def test_height_calculation_parsed_tree(self):
        tree = parse_code("print(1)")
        assert tree.metadata.height == 4

    def test_height_calculation_empty_tree(self):
        tree = Node("test", "", tuple())
        attach_metadata(tree)
        assert tree.metadata.height == 1

    def test_hash_calculation_small_isomorphic_trees(self):
        isomorphic1 = parse_code("print('foo');print('bar')")
        isomorphic2 = parse_code("print('foo'   )   ;       print('bar')")
        assert isomorphic1.isomorphic_to(isomorphic2)

    def test_hash_calculation_small_non_isomorphic_trees(self):
        foo_and_bar = parse_code("print('foo');print('bar')")
        bar = parse_code("print('bar')")
        assert not foo_and_bar.isomorphic_to(bar)

    def test_hash_calculation_isomorphic_trees(self):
        isomorphic1 = parse("tests/data/isomorphic1.py")
        isomorphic2 = parse("tests/data/isomorphic2.py")
        assert isomorphic1.isomorphic_to(isomorphic2)

    def test_hash_calculation_non_isomorphic_trees(self):
        test1 = parse("tests/data/test1.py")
        test2 = parse("tests/data/test2.py")
        assert not test1.isomorphic_to(test2)
