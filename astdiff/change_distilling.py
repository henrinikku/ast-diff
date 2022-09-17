import ast
import logging

logger = logging.getLogger(__name__)


class ChangeDistilling:
    def __init__(self, source_ast: ast.AST, target_ast: ast.AST):
        self.source_ast = source_ast
        self.target_ast = target_ast

    def diff(self):
        logger.info("Diffing...")
        logger.info("Source:\n%s", ast.dump(self.source_ast, indent=2))
        logger.info("Target:\n%s", ast.dump(self.target_ast, indent=2))
