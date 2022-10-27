from enum import Enum

from astdiff.matcher.base import ChangeDistillingMatcher, Matcher, StubMatcher
from astdiff.matcher.gumtree import GumTreeMatcher


class MatcherType(str, Enum):
    """
    Helper enum for choosing between different matcher implementations.
    """

    GUMTREE = "gumtree"
    STUB = "stub"
    CHANGE_DISTILLER = "change-distiller"


def build_matcher(matcher_type: MatcherType) -> Matcher:
    """
    Builds a matcher of the given type.
    """
    match matcher_type:
        case MatcherType.GUMTREE:
            return GumTreeMatcher()
        case MatcherType.STUB:
            return StubMatcher()
        case MatcherType.CHANGE_DISTILLER:
            return ChangeDistillingMatcher()
        case _:
            raise ValueError()
