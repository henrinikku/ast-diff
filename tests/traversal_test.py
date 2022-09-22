import unittest

from astdiff.ast import Node
from astdiff.traversal import post_order_walk, pre_order_walk


class TraversalTest(unittest.TestCase):
    def setUp(self):
        self.ast = Node(
            label="1a_label",
            value="1a_value",
            children=(
                Node(
                    label="2a_label",
                    value="2a_value",
                    children=(
                        Node(label="3a_label", value="3a_value", children=()),
                        Node(
                            label="3b_label",
                            value="3b_value",
                            children=(
                                Node(label="4a_label", value="4b_value", children=()),
                            ),
                        ),
                    ),
                ),
                Node(
                    label="2b_label",
                    value="2b_value",
                    children=(Node(label="2b_child_label", value="2b_child_value", children=()),),
                ),
            ),
        )

    def test_post_order_walk(self):
        nodes = [(x.label, x.value) for x in post_order_walk(self.ast)]

        self.assertEqual(
            nodes,
            [
                ("3a_label", "3a_value"),
                ("4a_label", "4b_value"),
                ("3b_label", "3b_value"),
                ("2a_label", "2a_value"),
                ("2b_child_label", "2b_child_value"),
                ("2b_label", "2b_value"),
                ("1a_label", "1a_value"),
            ],
        )

    def test_pre_order_walk(self):
        nodes = [(x.label, x.value) for x in pre_order_walk(self.ast)]

        self.assertEqual(
            nodes,
            [
                ("1a_label", "1a_value"),
                ("2a_label", "2a_value"),
                ("3a_label", "3a_value"),
                ("3b_label", "3b_value"),
                ("4a_label", "4b_value"),
                ("2b_label", "2b_value"),
                ("2b_child_label", "2b_child_value"),
            ],
        )
