import pytest

from astdiff.ast.metadata import add_parents, attach_metadata
from astdiff.ast.node import Node
from astdiff.context import DiffContext
from astdiff.editscript.generator import WithMoveEditScriptGenerator
from astdiff.matcher.gumtree import GumTreeMatcher
from astdiff.parser.base import ParseOptions
from astdiff.parser.parso import ParsoParser


@pytest.fixture(scope="function")
def parser():
    return ParsoParser(
        options=ParseOptions(
            add_metadata=True,
            add_parent=True,
        )
    )


@pytest.fixture(scope="function")
def no_metadata_parser():
    return ParsoParser(
        options=ParseOptions(
            add_metadata=False,
            add_parent=False,
        )
    )


@pytest.fixture(scope="function")
def matcher():
    return GumTreeMatcher()


@pytest.fixture(scope="function")
def generator():
    return WithMoveEditScriptGenerator()


@pytest.fixture(scope="function")
def source():
    """
    For visualization of the tree below, see figure 1 in page 4 of
    https://hal.archives-ouvertes.fr/hal-01054552/document
    """
    source_function_block = Node(
        label="Block",
        value="",
        children=(
            Node(
                label="IfStatement",
                value="",
                children=(
                    Node(
                        label="InfixExpression",
                        value="==",
                        children=(
                            Node(label="SimpleName", value="i", children=()),
                            Node(label="NumberLiteral", value="0", children=()),
                        ),
                    ),
                    Node(
                        label="ReturnStatement",
                        value="",
                        children=(
                            Node(label="StringLiteral", value="Foo!", children=()),
                        ),
                    ),
                ),
            ),
        ),
    )
    source_method_declaration = Node(
        label="MethodDeclaration",
        value="",
        children=(
            Node(label="Modifier", value="public", children=()),
            Node(
                label="SimpleType",
                value="String",
                children=(Node(label="SimpleName", value="String", children=()),),
            ),
            Node(label="SimpleName", value="foo", children=()),
            Node(
                label="SingleVariableDeclaration",
                value="",
                children=(
                    Node(
                        label="PrimitiveType",
                        value="int",
                        children=(),
                    ),
                    Node(label="SimpleName", value="i", children=()),
                ),
            ),
            source_function_block,
        ),
    )
    source = Node(
        label="CompilationUnit",
        value="",
        children=(
            Node(
                label="TypeDeclaration",
                value="",
                children=(
                    Node(label="Modifier", value="public", children=()),
                    Node(label="SimpleName", value="Test", children=()),
                    source_method_declaration,
                ),
            ),
        ),
    )

    add_parents(source)
    attach_metadata(source)

    return source


@pytest.fixture(scope="function")
def target():
    """
    For visualization of the tree below, see figure 1 in page 4 of
    https://hal.archives-ouvertes.fr/hal-01054552/document
    """
    target_function_else_if = Node(
        label="IfStatement",
        value="",
        children=(
            Node(
                label="InfixExpression",
                value="==",
                children=(
                    Node(
                        label="SimpleName",
                        value="i",
                        children=(),
                    ),
                    Node(
                        label="PrefixExpression",
                        value="-",
                        children=(
                            Node(
                                label="NumberLiteral",
                                value="1",
                                children=(),
                            ),
                        ),
                    ),
                ),
            ),
            Node(
                label="ReturnStatement",
                value="",
                children=(
                    Node(
                        label="StringLiteral",
                        value="Foo!",
                        children=(),
                    ),
                ),
            ),
        ),
    )
    target_function_block = Node(
        label="Block",
        value="",
        children=(
            Node(
                label="IfStatement",
                value="",
                children=(
                    Node(
                        label="InfixExpression",
                        value="==",
                        children=(
                            Node(label="SimpleName", value="i", children=()),
                            Node(label="NumberLiteral", value="0", children=()),
                        ),
                    ),
                    Node(
                        label="ReturnStatement",
                        value="",
                        children=(
                            Node(label="StringLiteral", value="Bar", children=()),
                        ),
                    ),
                    target_function_else_if,
                ),
            ),
        ),
    )

    target_method_declaration = Node(
        label="MethodDeclaration",
        value="",
        children=(
            Node(label="Modifier", value="private", children=()),
            Node(
                label="SimpleType",
                value="String",
                children=(Node(label="SimpleName", value="String", children=()),),
            ),
            Node(label="SimpleName", value="foo", children=()),
            Node(
                label="SingleVariableDeclaration",
                value="",
                children=(
                    Node(label="PrimitiveType", value="int", children=()),
                    Node(label="SimpleName", value="i", children=()),
                ),
            ),
            target_function_block,
        ),
    )
    target = Node(
        label="CompilationUnit",
        value="",
        children=(
            Node(
                label="TypeDeclaration",
                value="",
                children=(
                    Node(label="Modifier", value="public", children=()),
                    Node(label="SimpleName", value="Test", children=()),
                    target_method_declaration,
                ),
            ),
        ),
    )

    add_parents(target)
    attach_metadata(target)

    return target


@pytest.fixture(scope="function")
def post_matching_context(matcher: GumTreeMatcher, source: Node, target: Node):
    context = DiffContext(source, target)
    context.matching_set = matcher.find_matching_nodes(context)
    return context
