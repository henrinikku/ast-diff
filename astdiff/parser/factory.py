from enum import Enum

from astdiff.parser.base import ParseOptions, Parser
from astdiff.parser.builtin import BuiltInASTParser
from astdiff.parser.parso import ParsoParser


class ParserType(str, Enum):
    """
    Helper enum for choosing between different parser implementations.
    """

    PARSO = "parso"
    BUILTIN_AST = "builtin-ast"


def build_parser(parser_type: ParserType, options: ParseOptions) -> Parser:
    """
    Builds a parser of the given type with the given options.
    """
    match parser_type:
        case ParserType.PARSO:
            return ParsoParser(options)
        case ParserType.BUILTIN_AST:
            return BuiltInASTParser(options)
