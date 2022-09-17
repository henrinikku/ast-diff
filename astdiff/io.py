from ast import parse
from pathlib import Path


def read_ast(file_path: str):
    file_text = Path(file_path).read_text()
    return parse(file_text, filename=file_path)
