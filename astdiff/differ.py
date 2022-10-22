import logging

from astdiff.ast.node import Node
from astdiff.context import DiffContext
from astdiff.editscript.generator import (
    EditScriptGenerator,
    WithMoveEditScriptGenerator,
)
from astdiff.matcher.base import Matcher
from astdiff.matcher.gumtree import GumTreeMatcher

logger = logging.getLogger(__name__)


def diff(source_ast: Node, target_ast: Node):
    matcher = GumTreeMatcher()
    generator = WithMoveEditScriptGenerator()
    differ = Differ(matcher, generator)

    return differ.diff(source_ast, target_ast)


class Differ:
    def __init__(self, matcher: Matcher, generator: EditScriptGenerator):
        self.matcher = matcher
        self.generator = generator

    def diff(self, source_ast: Node, target_ast: Node):
        logger.debug("Diffing...")

        ctx = DiffContext(source_ast, target_ast)

        logger.debug(
            "%s + %s = %s nodes in total",
            len(ctx.source_nodes),
            len(ctx.target_nodes),
            len(ctx.source_nodes) + len(ctx.target_nodes),
        )

        logger.debug("Finding matching nodes...")
        ctx.matching_set = self.matcher.find_matching_nodes(ctx)

        logger.debug("Generating edit script...")
        ctx.edit_script = self.generator.generate_edit_script(ctx)

        logger.debug("Diffing done!")
        return ctx
