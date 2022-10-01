from astdiff.ast import Node
from astdiff.context import DiffContext, MatchingSet
from astdiff.gumtree import GumTreeMatcher
from astdiff.traversal import pre_order_walk


def get_matching_pairs(matching_set: MatchingSet, context: DiffContext):
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


def test_anchor_matching_performance(
    benchmark, matcher: GumTreeMatcher, source: Node, target: Node
):
    def setup():
        context = DiffContext(
            source_nodes={id(x): x for x in pre_order_walk(source)},
            target_nodes={id(x): x for x in pre_order_walk(target)},
        )
        matcher.prepare(context)

    def match_anchors():
        return matcher.match_anchors(source, target)

    benchmark.pedantic(match_anchors, setup=setup)


def test_container_matching_performance(
    benchmark, matcher: GumTreeMatcher, source: Node, target: Node
):
    def setup():
        context = DiffContext(
            source_nodes={id(x): x for x in pre_order_walk(source)},
            target_nodes={id(x): x for x in pre_order_walk(target)},
        )
        matcher.prepare(context)
        matcher.match_anchors(source, target)

    def match_containers():
        return matcher.match_containers(source, target)

    benchmark.pedantic(match_containers, setup=setup)


def test_anchor_matching(matcher: GumTreeMatcher, source: Node, target: Node):
    expected = [
        (("InfixExpression", "=="), ("InfixExpression", "==")),
        (("SimpleName", "i"), ("SimpleName", "i")),
        (("NumberLiteral", "0"), ("NumberLiteral", "0")),
        (("ReturnStatement", ""), ("ReturnStatement", "")),
        (("StringLiteral", "Foo!"), ("StringLiteral", "Foo!")),
        (("SimpleType", "String"), ("SimpleType", "String")),
        (("SimpleName", "String"), ("SimpleName", "String")),
        (("SingleVariableDeclaration", ""), ("SingleVariableDeclaration", "")),
        (("PrimitiveType", "int"), ("PrimitiveType", "int")),
        (("SimpleName", "i"), ("SimpleName", "i")),
    ]

    context = DiffContext(
        source_nodes={id(x): x for x in pre_order_walk(source)},
        target_nodes={id(x): x for x in pre_order_walk(target)},
    )
    matcher.prepare(context)

    matching_set = matcher.match_anchors(source, target)
    assert get_matching_pairs(matching_set, context) == expected

    flipped_context = DiffContext(
        source_nodes={id(x): x for x in pre_order_walk(target)},
        target_nodes={id(x): x for x in pre_order_walk(source)},
    )
    matcher.prepare(flipped_context)

    matching_set = matcher.match_anchors(target, source)
    assert get_matching_pairs(matching_set, flipped_context) == expected


def test_container_matching(matcher: GumTreeMatcher, source: Node, target: Node):
    expected = [
        (("IfStatement", ""), ("IfStatement", "")),
        (("Block", ""), ("Block", "")),
        (("MethodDeclaration", ""), ("MethodDeclaration", "")),
        (("TypeDeclaration", ""), ("TypeDeclaration", "")),
        (("CompilationUnit", ""), ("CompilationUnit", "")),
    ]

    context = DiffContext(
        source_nodes={id(x): x for x in pre_order_walk(source)},
        target_nodes={id(x): x for x in pre_order_walk(target)},
    )
    matcher.prepare(context)

    matched_anchors = get_matching_pairs(
        matcher.match_anchors(source, target),
        context,
    )
    matched_nodes = get_matching_pairs(
        matcher.match_containers(source, target),
        context,
    )
    matched_containers = matched_nodes[len(matched_anchors) :]
    assert matched_containers == expected

    flipped_context = DiffContext(
        source_nodes={id(x): x for x in pre_order_walk(target)},
        target_nodes={id(x): x for x in pre_order_walk(source)},
    )
    matcher.prepare(flipped_context)

    matched_anchors = get_matching_pairs(
        matcher.match_anchors(target, source),
        flipped_context,
    )
    matched_nodes = get_matching_pairs(
        matcher.match_containers(target, source),
        flipped_context,
    )
    matched_containers = matched_nodes[len(matched_anchors) :]
    assert matched_containers == expected
