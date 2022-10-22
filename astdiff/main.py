import logging

import typer

from astdiff.ast.parser import ParseOptions, ParsoParser
from astdiff.differ import diff as diff_asts

logger = logging.getLogger(__name__)

parser = ParsoParser(
    options=ParseOptions(
        add_metadata=True,
        add_parent=True,
    )
)

app = typer.Typer()


@app.command()
def diff(
    source: str,
    target: str,
    log_level: int = typer.Option(logging.INFO),
):
    """
    Prints an edit script which describes differences between
    syntax trees produced by source and target.
    """
    logging.basicConfig(level=log_level)

    logger.debug("Comparing '%s' and '%s'...", source, target)

    source_ast = parser.parse(source)
    target_ast = parser.parse(target)

    context = diff_asts(source_ast, target_ast)

    print(f"Edit script ({len(context.edit_script)} ops):")
    print(*context.edit_script.standalone(), sep="\n")


if __name__ == "__main__":
    app()
