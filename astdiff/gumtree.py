import ast

from astdiff.context import DiffContext
from astdiff.matcher import Matcher


class GumTreeMatcher(Matcher):
    """
    Implementation of the GumTree node matching algorithm.

    Source: Falleri et al. 2014
    https://hal.archives-ouvertes.fr/hal-01054552/document
    """

    def find_matching_nodes(
        self,
        source_ast: ast.AST,
        target_ast: ast.AST,
        ctx: DiffContext,
    ):
        raise NotImplementedError()

    
