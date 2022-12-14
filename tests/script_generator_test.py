from astdiff.ast.node import Node
from astdiff.context import DiffContext
from astdiff.editscript.ops import Insert, Move, Update
from astdiff.generator.with_move import WithMoveEditScriptGenerator


def test_edit_scrit_generation(
    generator: WithMoveEditScriptGenerator,
    post_matching_context: DiffContext,
):
    edit_script = generator.generate_edit_script(post_matching_context)

    # For now, edit operations are always applied to the source tree.
    assert post_matching_context.source_root == post_matching_context.target_root

    assert edit_script.standalone() == (
        Update(node=Node(label="Modifier", value="public"), value="private"),
        Insert(
            node=Node(label="ReturnStatement", value=""),
            parent=Node(label="IfStatement", value=""),
            position=1,
        ),
        Insert(
            node=Node(label="IfStatement", value=""),
            parent=Node(label="IfStatement", value=""),
            position=2,
        ),
        Insert(
            node=Node(label="StringLiteral", value="Bar"),
            parent=Node(label="ReturnStatement", value=""),
            position=0,
        ),
        Insert(
            node=Node(label="InfixExpression", value="=="),
            parent=Node(label="IfStatement", value=""),
            position=0,
        ),
        Move(
            node=Node(label="ReturnStatement", value=""),
            parent=Node(label="IfStatement", value=""),
            position=1,
        ),
        Insert(
            node=Node(label="SimpleName", value="i"),
            parent=Node(label="InfixExpression", value="=="),
            position=0,
        ),
        Insert(
            node=Node(label="PrefixExpression", value="-"),
            parent=Node(label="InfixExpression", value="=="),
            position=1,
        ),
        Insert(
            node=Node(label="NumberLiteral", value="1"),
            parent=Node(label="PrefixExpression", value="-"),
            position=0,
        ),
    )
