import ast_walker.functions


class ASTWalker:
    @staticmethod
    def execute(ast):
        from ast_walker.walker import ASTWalker as walker_stub
        from io import BytesIO

        walker_stub.execute(ast, BytesIO())
