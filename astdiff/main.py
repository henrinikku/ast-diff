import logging

import typer

from astdiff.differ import diff as diff_asts
from astdiff.util import read_ast

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def diff(
    source_file: str,
    target_file: str,
    log_level: int = typer.Option(logging.INFO),
):
    logging.basicConfig(level=log_level)

    logger.info("Comparing %s and %s...", source_file, target_file)

    source_ast = read_ast(source_file)
    target_ast = read_ast(target_file)

    edit_script = diff_asts(source_ast, target_ast)

    print(f"Edit script ({len(edit_script)} ops):")
    print(*edit_script, sep="\n")


if __name__ == "__main__":
    app()
