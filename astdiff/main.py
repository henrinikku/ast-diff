import logging

import typer

from astdiff.differ import diff as diff_asts
from astdiff.parse import parse, parse_code

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

    source_ast = parse(source) if source.endswith(".py") else parse_code(source)
    target_ast = parse(target) if target.endswith(".py") else parse_code(target)

    context = diff_asts(source_ast, target_ast)

    print(f"Edit script ({len(context.edit_script)} ops):")
    print(*context.edit_script, sep="\n")


if __name__ == "__main__":
    app()
