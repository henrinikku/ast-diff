from astdiff.ast.node import Node
from astdiff.context import DiffContext, MatchingSet
from astdiff.matcher.gumtree import GumTreeMatcher


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
        context = DiffContext(source, target)
        matcher.prepare(context)

    def match_anchors():
        return matcher.match_anchors(
            matcher.context.source_root, matcher.context.target_root
        )

    benchmark.pedantic(match_anchors, rounds=100, setup=setup)


def test_container_matching_performance(
    benchmark, matcher: GumTreeMatcher, source: Node, target: Node
):
    def setup():
        context = DiffContext(source, target)
        matcher.prepare(context)
        matcher.match_anchors(context.source_root, context.target_root)

    def match_containers():
        return matcher.match_containers(
            matcher.context.source_root, matcher.context.target_root
        )

    benchmark.pedantic(match_containers, rounds=100, setup=setup)


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

    context = DiffContext(source, target)
    matcher.prepare(context)

    matching_set = matcher.match_anchors(context.source_root, context.target_root)
    assert get_matching_pairs(matching_set, context) == expected

    flipped_context = DiffContext(target, source)
    matcher.prepare(flipped_context)

    matching_set = matcher.match_anchors(
        flipped_context.source_root, flipped_context.target_root
    )
    assert get_matching_pairs(matching_set, flipped_context) == expected


def test_container_matching(matcher: GumTreeMatcher, source: Node, target: Node):
    context = DiffContext(source, target)
    matcher.prepare(context)

    matched_anchors = get_matching_pairs(
        matcher.match_anchors(context.source_root, context.target_root),
        context,
    )
    matched_nodes = get_matching_pairs(
        matcher.match_containers(context.source_root, context.target_root),
        context,
    )
    matched_containers = matched_nodes[len(matched_anchors) :]
    assert matched_containers == [
        (("IfStatement", ""), ("IfStatement", "")),
        (("Block", ""), ("Block", "")),
        (("SimpleName", "foo"), ("SimpleName", "foo")),
        (("Modifier", "public"), ("Modifier", "private")),
        (("MethodDeclaration", ""), ("MethodDeclaration", "")),
        (("Modifier", "public"), ("Modifier", "public")),
        (("SimpleName", "Test"), ("SimpleName", "Test")),
        (("TypeDeclaration", ""), ("TypeDeclaration", "")),
        (("CompilationUnit", ""), ("CompilationUnit", "")),
    ]

    flipped_context = DiffContext(target, source)
    matcher.prepare(flipped_context)

    matched_anchors = get_matching_pairs(
        matcher.match_anchors(flipped_context.source_root, flipped_context.target_root),
        flipped_context,
    )
    matched_nodes = get_matching_pairs(
        matcher.match_containers(
            flipped_context.source_root, flipped_context.target_root
        ),
        flipped_context,
    )
    matched_containers = matched_nodes[len(matched_anchors) :]
    assert matched_containers == [
        (("IfStatement", ""), ("IfStatement", "")),
        (("Block", ""), ("Block", "")),
        (("SimpleName", "foo"), ("SimpleName", "foo")),
        (("Modifier", "private"), ("Modifier", "public")),
        (("MethodDeclaration", ""), ("MethodDeclaration", "")),
        (("Modifier", "public"), ("Modifier", "public")),
        (("SimpleName", "Test"), ("SimpleName", "Test")),
        (("TypeDeclaration", ""), ("TypeDeclaration", "")),
        (("CompilationUnit", ""), ("CompilationUnit", "")),
    ]
