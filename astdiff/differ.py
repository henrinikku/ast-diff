import logging

from astdiff.ast.node import Node
from astdiff.context import DiffContext
from astdiff.generator.base import EditScriptGenerator
from astdiff.generator.with_move import WithMoveEditScriptGenerator
from astdiff.matcher.base import Matcher
from astdiff.matcher.gumtree import GumTreeMatcher

logger = logging.getLogger(__name__)


def diff(source_ast: Node, target_ast: Node):
    """
    Returns a diff of given ASTs using GumTreeMatcher and WithMoveEditScriptGenerator.
    """
    matcher = GumTreeMatcher()
    generator = WithMoveEditScriptGenerator()
    differ = Differ(matcher, generator)

    return differ.diff(source_ast, target_ast)


class Differ:
    """
    Implements AST diffing using given node matcher and edit script generator.
    """

    def __init__(self, matcher: Matcher, generator: EditScriptGenerator):
        self.matcher = matcher
        self.generator = generator

    def diff(self, source_ast: Node, target_ast: Node):
        """
        Returns a context containing the diff between given ASTs.
        """
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
