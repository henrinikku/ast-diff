import logging
from abc import ABC, abstractmethod

from astdiff.context import DiffContext, MatchingPair
from astdiff.edit_script import Delete, EditScript, Insert, Move, Update

logger = logging.getLogger(__name__)


class EditScriptGenerator(ABC):
    """
    Base class for all edit script generator implementations.
    Some implementations might for example consider move operations and some might not.
    """

    @abstractmethod
    def generate_edit_script(self, context: DiffContext) -> EditScript:
        ...


class WithMoveEditScriptGenerator(EditScriptGenerator):
    """
    Edit script generator that takes into account moved nodes.

    Source: Chawathe et al. 1996 https://dl.acm.org/doi/pdf/10.1145/235968.233366
    """

    def generate_edit_script(self, context: DiffContext):
        logger.debug(
            "Matched nodes:\n%s",
            "\n,".join(
                [
                    str((x.standalone(), y.standalone()))
                    for x, y in context.matched_nodes
                ]
            ),
        )

        matched_pairs = set(context.matching_set.pairs)

        matched_source_ids = set(context.matching_set.source_target_map)
        matched_target_ids = set(context.matching_set.target_source_map)

        ops = []

        ops += (
            Delete(context.source_nodes[x].standalone())
            for x in set(context.source_nodes) - matched_source_ids
        )

        ops += (
            Insert(context.target_nodes[x].standalone())
            for x in set(context.target_nodes) - matched_target_ids
        )

        ops += (
            Update(source.standalone(), target.standalone())
            for source, target in context.matched_nodes
            if source.value != target.value
        )

        # TODO: Add align phase

        ops += (
            Move(
                source.standalone(),
                source.parent.standalone(),
                target.parent.standalone(),
            )
            for source, target in context.matched_nodes
            if (source.parent or target.parent)
            and MatchingPair(id(source.parent), id(target.parent)) not in matched_pairs
        )

        return tuple(ops)
