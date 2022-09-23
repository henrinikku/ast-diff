from abc import ABC, abstractmethod

from astdiff.context import DiffContext
from astdiff.edit_script import Delete, EditScript, Insert, Move, Update


class EditScriptGenerator(ABC):
    """
    Base class for all edit script generator implementations.
    Some implementations might for example consider move operations and some might not.
    """

    @abstractmethod
    def generate_edit_script(self, ctx: DiffContext) -> EditScript:
        ...


class WithMoveEditScriptGenerator(EditScriptGenerator):
    """
    Edit script generator that takes into account moved nodes.

    Source: Chawathe et al. 1996 https://dl.acm.org/doi/pdf/10.1145/235968.233366
    """

    def generate_edit_script(self, ctx: DiffContext):
        ops = []

        inserted_ids = ctx.unmatched_target_ids
        ops += [Insert(ctx.target_nodes[x].standalone()) for x in inserted_ids]

        deleted_ids = ctx.unmatched_source_ids
        ops += [Delete(ctx.source_nodes[x].standalone()) for x in deleted_ids]

        # TODO: Generate moves and updates
        return tuple(ops)
