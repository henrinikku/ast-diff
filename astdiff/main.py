import logging

import typer

from astdiff.differ import Differ
from astdiff.generator.factory import (
    EditScriptGeneratorType,
    build_edit_script_generator,
)
from astdiff.matcher.factory import MatcherType, build_matcher
from astdiff.parser.base import ParseOptions
from astdiff.parser.factory import ParserType, build_parser

logger = logging.getLogger(__name__)

parse_options = ParseOptions(
    add_metadata=True,
    add_parent=True,
)

app = typer.Typer()


@app.command()
def diff(
    source: str,
    target: str,
    parser_type: ParserType = typer.Option(ParserType.BUILTIN_AST),
    matcher_type: MatcherType = typer.Option(MatcherType.GUMTREE),
    script_generator_type: EditScriptGeneratorType = typer.Option(
        EditScriptGeneratorType.WITH_MOVE
    ),
    log_level: int = typer.Option(logging.INFO),
):
    """
    Prints an edit script which describes differences between
    syntax trees produced by source and target.
    """
    logging.basicConfig(level=log_level)

    logger.debug("Comparing '%s' and '%s'...", source, target)

    parser = build_parser(parser_type, parse_options)
    source_ast = parser.parse(source)
    target_ast = parser.parse(target)

    matcher = build_matcher(matcher_type)
    generator = build_edit_script_generator(script_generator_type)
    differ = Differ(matcher, generator)

    context = differ.diff(source_ast, target_ast)

    print(f"Edit script ({len(context.edit_script)} ops):")
    print(*context.edit_script.standalone(), sep="\n")


if __name__ == "__main__":
    app()
