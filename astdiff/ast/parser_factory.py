from enum import Enum
from typing import Callable, Dict

from astdiff.ast.parser import BuiltInASTParser, ParseOptions, Parser, ParsoParser


class ParserType(str, Enum):
    parso = "parso"
    builtin_ast = "builtin-ast"


PARSER_FACTORY_MAP: Dict[ParserType, Callable[[ParseOptions], Parser]] = {
    ParserType.parso: ParsoParser,
    ParserType.builtin_ast: BuiltInASTParser,
}


def build_parser(parser_type: ParserType, options: ParseOptions):
    factory_fn = PARSER_FACTORY_MAP[parser_type]
    return factory_fn(options)
