from astdiff.context import DiffContext
from astdiff.script_generator import WithMoveEditScriptGenerator


def test_edit_scrit_generation(
    generator: WithMoveEditScriptGenerator,
    post_matching_context: DiffContext,
):
    edit_script = generator.generate_edit_script(post_matching_context)
    print(*edit_script, sep=",\n")
    # TODO
    assert bool(edit_script)
