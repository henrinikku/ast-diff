import logging
from abc import ABC, abstractmethod

from astdiff.context import DiffContext
from astdiff.editscript import EditScript

logger = logging.getLogger(__name__)


class EditScriptGenerator(ABC):
    """
    Base class for all edit script generator implementations.
    Some implementations might for example consider move operations and some might not.
    """

    @abstractmethod
    def generate_edit_script(self, context: DiffContext) -> EditScript:
        ...
