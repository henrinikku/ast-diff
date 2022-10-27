from typing import Tuple

from astdiff.editscript.ops import Operation


class EditScript(Tuple[Operation, ...]):
    """
    Represents an edit script, i.e., a tuple of edit operations.
    """

    def standalone(self):
        """
        Returns a copy of self with references to standalone nodes.
        """
        return EditScript(op.standalone() for op in self)
