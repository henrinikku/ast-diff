from enum import Enum
from typing import Callable, Dict

from astdiff.parser.base import ParseOptions, Parser
from astdiff.parser.builtin import BuiltInASTParser
from astdiff.parser.parso import ParsoParser


class ParserType(str, Enum):
    parso = "parso"
    builtin_ast = "builtin-ast"


ParserFactoryFn = Callable[[ParseOptions], Parser]

PARSER_TYPE_FACTORY_MAP: Dict[ParserType, ParserFactoryFn] = {
    ParserType.parso: ParsoParser,
    ParserType.builtin_ast: BuiltInASTParser,
}


def build_parser(parser_type: ParserType, options: ParseOptions):
    factory_fn = PARSER_TYPE_FACTORY_MAP[parser_type]
    return factory_fn(options)
