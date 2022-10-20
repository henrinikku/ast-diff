import logging
from abc import ABC, abstractmethod
from itertools import product
from typing import List, Set

from more_itertools import first

from astdiff.ast import Node
from astdiff.context import DiffContext, MatchingPair, NodeId
from astdiff.edit_script import Delete, EditScript, Insert, Move, Operation, Update
from astdiff.traversal import bfs, post_order_walk
from astdiff.util import longest_common_subsequence

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

    def prepare(self, context: DiffContext):
        logger.debug(
            "Matched nodes:\n%s",
            "\n".join([str((x, y)) for x, y in context.matched_nodes]),
        )

        # TODO: Deep copy context before applying changes
        self.context = context
        self.in_order: Set[NodeId] = set()
        self.ops: List[Operation] = []

    def generate_edit_script(self, context: DiffContext):
        self.prepare(context)

        for target in bfs(context.target_root):
            source = context.partner(target)
            # The partner of target's parent, i.e., a source node.
            source_parent = target.parent and context.partner(target.parent)

            if source is None:
                position = self._find_position(target)
                source = Node(target.label, target.value)
                insert = Insert(source, source_parent, position)
                insert.apply()
                self.ops.append(insert)
                context.add_source(source)
                context.matching_set.add(MatchingPair(id(source), id(target)))

            elif not target.is_root:
                if source.value != target.value:
                    update = Update(source, target)
                    update.apply()
                    self.ops.append(update)

                if context.partner(source.parent) is not target.parent:
                    position = self._find_position(target)
                    move = Move(source, source_parent, position)
                    move.apply()
                    self.ops.append(move)

            self.in_order.update((id(source), id(target)))
            self._align_children(source, target)

        for source in post_order_walk(context.source_root):
            if id(source) not in self.context.matching_set.source_target_map:
                delete = Delete(source)
                delete.apply()
                self.ops.append(delete)
                context.remove_source(source)

        return EditScript(self.ops)

    def _align_children(self, source: Node, target: Node):
        source_children = list(map(id, source.children))
        target_children = list(map(id, target.children))

        self.in_order -= set(source_children)
        self.in_order -= set(target_children)

        matched_source_children = [
            self.context.source_nodes[x]
            for x in source_children
            if self.context.matching_set.source_target_map.get(x) in target_children
        ]
        matched_target_children = [
            self.context.target_nodes[x]
            for x in target_children
            if self.context.matching_set.target_source_map.get(x) in source_children
        ]

        # Use dict to preserve order for easier debugging.
        longest_common_subseq = dict.fromkeys(
            (id(s), id(t))
            for s, t in longest_common_subsequence(
                matched_source_children,
                matched_target_children,
                lambda a, b: self.context.partner(a) is b,
            )
        )

        # Mark each node in the lcs as "in order".
        self.in_order.update(*longest_common_subseq)

        for target_child, source_child in product(
            matched_target_children, matched_source_children
        ):
            child_pair = id(source_child), id(target_child)
            # Realign all matches that are not part of the lcs.
            if (
                self.context.partner(source_child) is target_child
                and child_pair not in longest_common_subseq
            ):
                Delete(source_child).apply()
                position = self._find_position(target_child)
                Insert(source_child, source, position).apply()
                self.ops.append(Move(source_child, source, position))
                self.in_order.update(child_pair)

    def _find_position(self, target: Node):
        in_order_siblings = [
            target_sibling
            for target_sibling in target.siblings
            if id(target_sibling) in self.in_order
        ]

        if not in_order_siblings or target is first(in_order_siblings, None):
            return 0

        rightmost = None
        for sibling in in_order_siblings:
            if sibling is target:
                break
            rightmost = sibling

        source = self.context.partner(rightmost)
        return 0 if source is None else source.position + 1
