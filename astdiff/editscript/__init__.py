from typing import Tuple

from astdiff.editscript.ops import Operation


class EditScript(Tuple[Operation, ...]):
    def standalone(self):
        return EditScript(op.standalone() for op in self)
