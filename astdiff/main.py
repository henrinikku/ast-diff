import typer
import logging
from pathlib import Path

from astdiff.change_distilling import ChangeDistilling
from astdiff.io import read_ast

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

    differ = ChangeDistilling(source_ast, target_ast)
    differ.diff()



if __name__ == "__main__":
    app()
