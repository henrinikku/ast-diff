from functools import partial

import pytest

from astdiff.ast import Node
from astdiff.context import DiffContext
from astdiff.gumtree import GumTreeMatcher
from astdiff.metadata import attach_metadata
from astdiff.parser import Parser
from astdiff.traversal import pre_order_walk


@pytest.fixture(scope="function")
def python_source_200_lines(parser: Parser):
    return parser.parse_file("tests/data/django_serializer_19e0587.py")


@pytest.fixture(scope="function")
def python_target_200_lines(parser: Parser):
    return parser.parse_file("tests/data/django_serializer_8f30556.py")


@pytest.fixture(scope="function")
def python_source_2k_lines(parser: Parser):
    return parser.parse_file("tests/data/2k_lines_source.py")


@pytest.fixture(scope="function")
def python_target_2k_lines(parser: Parser):
    return parser.parse_file("tests/data/2k_lines_target.py")


def test_metadata_calculation_performance_200_lines(
    benchmark, no_metadata_parser: Parser
):
    source = no_metadata_parser.parse_file("tests/data/django_serializer_19e0587.py")
    benchmark(partial(attach_metadata, source))


def test_metadata_calculation_performance_2k_lines(
    benchmark, no_metadata_parser: Parser
):
    source = no_metadata_parser.parse_file("tests/data/2k_lines_source.py")
    benchmark(partial(attach_metadata, source))


def test_gumtree_performance_200_lines(
    benchmark,
    matcher: GumTreeMatcher,
    python_source_200_lines: Node,
    python_target_200_lines: Node,
):
    def setup():
        context = DiffContext(
            source_nodes={id(x): x for x in pre_order_walk(python_source_200_lines)},
            target_nodes={id(x): x for x in pre_order_walk(python_target_200_lines)},
        )
        matcher.prepare(context)

    def match_nodes():
        return matcher.find_matching_nodes(matcher.context)

    benchmark.pedantic(match_nodes, rounds=10, setup=setup)


def test_gumtree_performance_2k_lines(
    benchmark,
    matcher: GumTreeMatcher,
    python_source_2k_lines: Node,
    python_target_2k_lines: Node,
):
    def setup():
        context = DiffContext(
            source_nodes={id(x): x for x in pre_order_walk(python_source_2k_lines)},
            target_nodes={id(x): x for x in pre_order_walk(python_target_2k_lines)},
        )
        matcher.prepare(context)

    def match_nodes():
        return matcher.find_matching_nodes(matcher.context)

    benchmark.pedantic(match_nodes, rounds=3, setup=setup)
