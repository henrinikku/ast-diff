import unittest

from astdiff.ast import Node
from astdiff.context import DiffContext, MatchingSet
from astdiff.gumtree import GumTreeMatcher
from astdiff.metadata import add_parents, attach_metadata
from astdiff.traversal import pre_order_walk


class GumTreeMatcherTest(unittest.TestCase):
    def setUp(self):
        """
        For visualization of the tree below, see page 4 of
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

        add_parents(self.source)
        add_parents(self.target)

        attach_metadata(self.source)
        attach_metadata(self.target)

        self.matcher = GumTreeMatcher(min_height=1)

    def get_matching_pairs(self, matching_set: MatchingSet, context: DiffContext):
        return [
            (
                (
                    context.source_nodes[x.source].label,
                    context.source_nodes[x.source].value,
                ),
                (
                    context.target_nodes[x.target].label,
                    context.target_nodes[x.target].value,
                ),
            )
            for x in matching_set.pairs
        ]

    def test_anchor_matching(self):
        expected = sorted(
            [
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
        )

        context = DiffContext(
            source_nodes={id(x): x for x in pre_order_walk(self.source)},
            target_nodes={id(x): x for x in pre_order_walk(self.target)},
        )
        self.matcher.prepare(context)

        matching_set = self.matcher.match_anchors(self.source, self.target)
        assert sorted(self.get_matching_pairs(matching_set, context)) == expected

        flipped_context = DiffContext(
            source_nodes={id(x): x for x in pre_order_walk(self.target)},
            target_nodes={id(x): x for x in pre_order_walk(self.source)},
        )
        self.matcher.prepare(flipped_context)

        matching_set = self.matcher.match_anchors(self.target, self.source)
        assert (
            sorted(self.get_matching_pairs(matching_set, flipped_context)) == expected
        )
