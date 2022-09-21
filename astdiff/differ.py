import ast
import logging

from astdiff.context import DiffContext
from astdiff.edit_script import (
    EditScript,
    EditScriptGenerator,
    WithMoveEditScriptGenerator,
)
from astdiff.matcher import Matcher, StubMatcher
from astdiff.transform import add_metadata

logger = logging.getLogger(__name__)


def diff(source_ast: ast.AST, target_ast: ast.AST):
    # Add metadata (e.g. label, is_leaf) to nodes.
    add_metadata(source_ast)
    add_metadata(target_ast)

    matcher = StubMatcher()
    generator = WithMoveEditScriptGenerator()
    differ = Differ(matcher, generator)

    return differ.diff(source_ast, target_ast)


class Differ:
    def __init__(self, matcher: Matcher, generator: EditScriptGenerator):
        self.matcher = matcher
        self.generator = generator

    def diff(self, source_ast: ast.AST, target_ast: ast.AST) -> EditScript:
        logger.debug("Diffing...")

        ctx = DiffContext(
            source_nodes={id(x): x for x in ast.walk(source_ast)},
            target_nodes={id(x): x for x in ast.walk(target_ast)},
            matching_set=frozenset(),
        )

        logger.debug("Source:\n%s", ast.dump(source_ast, indent=4))
        logger.debug("Target:\n%s", ast.dump(target_ast, indent=4))
        logger.debug(
            "%s + %s = %s nodes in total",
            len(ctx.source_nodes),
            len(ctx.target_nodes),
            len(ctx.source_nodes) + len(ctx.target_nodes),
        )

        logger.debug("Finding matching nodes...")
        matching_set = self.matcher.find_matching_nodes(source_ast, target_ast, ctx)
        ctx = ctx.copy(matching_set=matching_set)

        logger.debug("Generating edit script...")
        edit_script = self.generator.generate_edit_script(ctx)

        logger.debug("Diffing done!")
        return edit_script
