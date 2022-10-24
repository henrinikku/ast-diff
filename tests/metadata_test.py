from astdiff.ast.metadata import attach_metadata
from astdiff.ast.node import Node
from astdiff.parser.parso import ParsoParser


def test_size_calculation_parsed_tree(parser: ParsoParser):
    tree = parser.parse_code("print(1)")
    assert tree.metadata.size == 5


def test_size_calculation_empty_tree():
    tree = Node("test", "", tuple())
    attach_metadata(tree)
    assert tree.metadata.size == 1


def test_height_calculation_parsed_tree(parser: ParsoParser):
    tree = parser.parse_code("print(1)")
    assert tree.metadata.height == 4


def test_height_calculation_empty_tree():
    tree = Node("test", "", tuple())
    attach_metadata(tree)
    assert tree.metadata.height == 1


def test_hash_calculation_small_isomorphic_trees(parser: ParsoParser):
    isomorphic1 = parser.parse_code("print('foo');print('bar')")
    isomorphic2 = parser.parse_code("print('foo'   )   ;       print('bar')")
    assert isomorphic1.isomorphic_to(isomorphic2)


def test_hash_calculation_small_non_isomorphic_trees(parser: ParsoParser):
    foo_and_bar = parser.parse_code("print('foo');print('bar')")
    bar = parser.parse_code("print('bar')")
    assert not foo_and_bar.isomorphic_to(bar)


def test_hash_calculation_isomorphic_trees(parser: ParsoParser):
    isomorphic1 = parser.parse("tests/data/isomorphic1.py")
    isomorphic2 = parser.parse("tests/data/isomorphic2.py")
    assert isomorphic1.isomorphic_to(isomorphic2)


def test_hash_calculation_non_isomorphic_trees(parser: ParsoParser):
    test1 = parser.parse("tests/data/test1.py")
    test2 = parser.parse("tests/data/test2.py")
    assert not test1.isomorphic_to(test2)
