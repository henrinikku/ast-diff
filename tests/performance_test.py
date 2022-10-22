from functools import partial

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from astdiff.ast.metadata import attach_metadata
from astdiff.ast.node import Node
from astdiff.ast.parser import Parser
from astdiff.context import DiffContext
from astdiff.editscript.generator import WithMoveEditScriptGenerator
from astdiff.matcher.gumtree import GumTreeMatcher


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
    benchmark: BenchmarkFixture,
    matcher: GumTreeMatcher,
    python_source_200_lines: Node,
    python_target_200_lines: Node,
):
    def setup():
        context = DiffContext(python_source_200_lines, python_target_200_lines)
        return [context], {}

    benchmark.pedantic(matcher.find_matching_nodes, rounds=10, setup=setup)


def test_gumtree_performance_2k_lines(
    benchmark: BenchmarkFixture,
    matcher: GumTreeMatcher,
    python_source_2k_lines: Node,
    python_target_2k_lines: Node,
):
    def setup():
        context = DiffContext(python_source_2k_lines, python_target_2k_lines)
        return [context], {}

    benchmark.pedantic(matcher.find_matching_nodes, rounds=3, setup=setup)


def test_edit_script_generation_performance_200_lines(
    benchmark: BenchmarkFixture,
    matcher: GumTreeMatcher,
    generator: WithMoveEditScriptGenerator,
    python_source_200_lines: Node,
    python_target_200_lines: Node,
):
    def setup():
        context = DiffContext(python_source_200_lines, python_target_200_lines)
        context.matching_set = matcher.find_matching_nodes(context)
        return [context], {}

    benchmark.pedantic(generator.generate_edit_script, rounds=10, setup=setup)


def test_edit_script_generation_performance_2k_lines(
    benchmark: BenchmarkFixture,
    matcher: GumTreeMatcher,
    generator: WithMoveEditScriptGenerator,
    python_source_2k_lines: Node,
    python_target_2k_lines: Node,
):
    def setup():
        context = DiffContext(python_source_2k_lines, python_target_2k_lines)
        context.matching_set = matcher.find_matching_nodes(context)
        return [context], {}

    benchmark.pedantic(generator.generate_edit_script, rounds=3, setup=setup)


def test_diff_performance_200_lines(
    benchmark: BenchmarkFixture,
    matcher: GumTreeMatcher,
    generator: WithMoveEditScriptGenerator,
    python_source_200_lines: Node,
    python_target_200_lines: Node,
):
    def setup():
        context = DiffContext(python_source_200_lines, python_target_200_lines)
        return [context], {}

    def diff(context: DiffContext):
        context.matching_set = matcher.find_matching_nodes(context)
        context.edit_script = generator.generate_edit_script(context)
        return context

    benchmark.pedantic(diff, rounds=3, setup=setup)


def test_diff_performance_2k_lines(
    benchmark: BenchmarkFixture,
    matcher: GumTreeMatcher,
    generator: WithMoveEditScriptGenerator,
    python_source_2k_lines: Node,
    python_target_2k_lines: Node,
):
    def setup():
        context = DiffContext(python_source_2k_lines, python_target_2k_lines)
        return [context], {}

    def diff(context: DiffContext):
        context.matching_set = matcher.find_matching_nodes(context)
        context.edit_script = generator.generate_edit_script(context)
        return context

    benchmark.pedantic(diff, rounds=3, setup=setup)
