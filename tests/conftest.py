import pytest

from astdiff.ast import Node
from astdiff.gumtree import GumTreeMatcher
from astdiff.metadata import add_parents, attach_metadata


@pytest.fixture(scope="session")
def matcher():
    return GumTreeMatcher()


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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