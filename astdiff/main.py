import logging

import typer

from astdiff.ast.parser import ParseOptions
from astdiff.ast.parser_factory import ParserType, build_parser
from astdiff.differ import diff as diff_asts

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
    parser_type: ParserType = typer.Option(ParserType.builtin_ast),
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

    context = diff_asts(source_ast, target_ast)

    print(f"Edit script ({len(context.edit_script)} ops):")
    print(*context.edit_script.standalone(), sep="\n")


if __name__ == "__main__":
    app()
