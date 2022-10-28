from enum import Enum

from astdiff.generator.base import EditScriptGenerator
from astdiff.generator.with_move import WithMoveEditScriptGenerator


class EditScriptGeneratorType(str, Enum):
    """
    Helper enum for choosing between different edit script generator implementations.
    """

    WITH_MOVE = "with-move"


def build_edit_script_generator(
    script_generator_type: EditScriptGeneratorType,
) -> EditScriptGenerator:
    """
    Builds an edit script generator of the given type.
    """
    match script_generator_type:
        case EditScriptGeneratorType.WITH_MOVE:
            return WithMoveEditScriptGenerator()
