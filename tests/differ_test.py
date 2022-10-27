from astdiff.ast.node import Node
from astdiff.differ import diff
from astdiff.editscript.ops import Delete, Move, Update
from astdiff.parser.builtin import BuiltInASTParser
from astdiff.parser.parso import ParsoParser


def test_diff(parser: ParsoParser):
    source_ast = parser.parse_code("print('123')")
    target_ast = parser.parse_code("print(\n'321')")
    context = diff(source_ast, target_ast)

    assert context.source_root == context.target_root
    assert context.edit_script.standalone() == (
        Update(node=Node(label="string", value="'123'"), value="'321'"),
    )


def test_diff_same_small_file(parser: ParsoParser):
    source_ast = parser.parse("tests/data/test1.py")
    target_ast = parser.parse("tests/data/test1.py")
    context = diff(source_ast, target_ast)

    assert context.source_root == context.target_root
    assert not context.edit_script


def test_diff_small_file(parser: ParsoParser):
    source_ast = parser.parse("tests/data/test1.py")
    target_ast = parser.parse("tests/data/test2.py")
    context = diff(source_ast, target_ast)

    assert context.source_root == context.target_root
    assert context.edit_script.standalone() == (
        Update(node=Node(label="string", value='"test1"'), value='"test2"'),
        Delete(node=Node(label="keyword", value="import")),
        Delete(node=Node(label="name", value="os")),
        Delete(node=Node(label="import_name", value="")),
        Delete(node=Node(label="simple_stmt", value="")),
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


def test_diff_move_update_builtin_parser(builtin_parser: BuiltInASTParser):
    source_ast = builtin_parser.parse("tests/data/moveupdate1.py")
    target_ast = builtin_parser.parse("tests/data/moveupdate2.py")
    context = diff(source_ast, target_ast)

    assert context.source_root == context.target_root
    assert context.edit_script.standalone() == (
        Move(
            node=Node(label="Expr", value=""),
            parent=Node(label="Module", value=""),
            position=2,
        ),
        Update(node=Node(label="alias", value="os"), value="logging"),
    )
