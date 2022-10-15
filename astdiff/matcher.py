import logging
from abc import ABC, abstractmethod

from astdiff.context import DiffContext, MatchingSet

logger = logging.getLogger(__name__)


class Matcher(ABC):
    """
    Base class for all node matching implementations.
    """

    @abstractmethod
    def find_matching_nodes(self, context: DiffContext) -> MatchingSet:
        ...


class StubMatcher(Matcher):
    """
    Dummy matcher that never matches any nodes.
    """

    def find_matching_nodes(self, context: DiffContext):
        return MatchingSet()


class ChangeDistillingMatcher(Matcher):
    """
    Implementation of the Change Distilling algorithm for node matching.

    Not implemented for now since the algorithm requires a simplified version of AST
    which is very different from what easily available parsers can offer.

    Source: Fluri et al. 2007
    http://serg.aau.at/pub/MartinPinzger/Publications/Fluri2007-changedistiller.pdf
    """

    def find_matching_nodes(self, context: DiffContext):
        raise NotImplementedError()
