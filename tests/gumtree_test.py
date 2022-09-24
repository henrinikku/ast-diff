import unittest

from astdiff.ast import Node
from astdiff.context import DiffContext, MatchingSet
from astdiff.gumtree import GumTreeMatcher
from astdiff.metadata import attach_metadata
from astdiff.traversal import post_order_walk, pre_order_walk


def _add_parents(tree: Node):
    for node in post_order_walk(tree):
        for child in node.children:
            child.parent = node


class GumTreeMatcherTest(unittest.TestCase):
    def setUp(self):
        """
        For visualization of the tree below, see page 4.
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
        self.source = Node(
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
        self.target = Node(
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

        _add_parents(self.source)
        _add_parents(self.target)

        attach_metadata(self.source)
        attach_metadata(self.target)

        self.context = DiffContext(
            source_nodes={id(x): x for x in pre_order_walk(self.source)},
            target_nodes={id(x): x for x in pre_order_walk(self.target)},
            matching_set=MatchingSet(),
            edit_script=(),
        )

        self.matcher = GumTreeMatcher(min_height=1)

    def test_anchor_matching(self):
        matching_set = self.matcher.match_anchors(
            self.source, self.target, self.context
        )

        matching_pairs = [
            (
                (
                    self.context.source_nodes[x.source].label,
                    self.context.source_nodes[x.source].value,
                ),
                (
                    self.context.target_nodes[x.target].label,
                    self.context.target_nodes[x.target].value,
                ),
            )
            for x in matching_set.pairs
        ]

        assert list(sorted(matching_pairs)) == [
            (("InfixExpression", "=="), ("InfixExpression", "==")),
            (("Modifier", "public"), ("Modifier", "public")),
            (("NumberLiteral", "0"), ("NumberLiteral", "0")),
            (("PrimitiveType", "int"), ("PrimitiveType", "int")),
            (("ReturnStatement", ""), ("ReturnStatement", "")),
            (("SimpleName", "String"), ("SimpleName", "String")),
            (("SimpleName", "Test"), ("SimpleName", "Test")),
            (("SimpleName", "foo"), ("SimpleName", "foo")),
            (("SimpleName", "i"), ("SimpleName", "i")),
            (("SimpleName", "i"), ("SimpleName", "i")),
            (("SimpleType", "String"), ("SimpleType", "String")),
            (("SingleVariableDeclaration", ""), ("SingleVariableDeclaration", "")),
            (("StringLiteral", "Foo!"), ("StringLiteral", "Foo!")),
        ]
