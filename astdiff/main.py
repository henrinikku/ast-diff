import logging

import typer

from astdiff.differ import diff as diff_asts
from astdiff.parse import ParseOptions, parse, parse_code

PARSE_OPTIONS = ParseOptions(
    add_metadata=True,
    add_parent=True,
)

logger = logging.getLogger(__name__)


app = typer.Typer()


@app.command()
def diff(
    source: str,
    target: str,
    log_level: int = typer.Option(logging.INFO),
):
    logging.basicConfig(level=log_level)

    logger.info("Comparing '%s' and '%s'...", source, target)

    source_ast = _parse_input(source)
    target_ast = _parse_input(target)

    context = diff_asts(source_ast, target_ast)

    print(f"Edit script ({len(context.edit_script)} ops):")
    print(*context.edit_script, sep="\n")


def _parse_input(input: str):
    return (
        parse(input, PARSE_OPTIONS)
        if input.endswith(".py")
        else parse_code(input, PARSE_OPTIONS)
    )


if __name__ == "__main__":
    app()
