from astdiff.ast import Node
from astdiff.differ import diff
from astdiff.edit_script import Update
from astdiff.parser import ParsoParser


def test_diff(parser: ParsoParser):
    source_ast = parser.parse_code("print('123')")
    target_ast = parser.parse_code("print(\n'321')")
    context = diff(source_ast, target_ast)

    assert context.source_root == context.target_root

    assert context.edit_script.standalone() == (
        Update(node=Node(label="string", value="'123'"), value="'321'"),
    )


def test_diff_empty_file(parser: ParsoParser):
    source_ast = parser.parse("tests/data/empty.py")
    target_ast = parser.parse("tests/data/empty.py")
    context = diff(source_ast, target_ast)

    assert context.source_root == context.target_root
    assert not context.edit_script


def test_diff_empty_and_whitespace(parser: ParsoParser):
    source_ast = parser.parse("tests/data/empty.py")
    target_ast = parser.parse("tests/data/whitespace.py")
    context = diff(source_ast, target_ast)

    assert context.source_root == context.target_root
    assert not context.edit_script
