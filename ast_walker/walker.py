from io import BytesIO
from ast_walker.executor import FunctionExecutor
from environment import EnvironmentHandler


class ASTWalker:
    '''
        A class that walks the passed AST
    '''
    @staticmethod
    def execute(ast, input_stream):
        '''
            executes the AST with the transmitted input stream
        '''

        if len(ast) == 0:
            return 0, BytesIO(), BytesIO() # empty input


        command = ast[0]

        if command == 'pipe':
            left, right = ast[1:]

            returncode_left, out_left, err_left = ASTWalker.execute(left, BytesIO())

            if returncode_left != 0:
                return returncode_left, out_left, err_left

            returncode_right, out_right, err_right = ASTWalker.execute(right, out_left)

            returncode = returncode_right
            out = out_right
            err = err_left
            err.write(err_right.getvalue())

            return returncode, out, err
        elif command == "assign":
            var = ast[1]
            val = ast[2]
            EnvironmentHandler.set_value(var, val)

            return 0, BytesIO(), BytesIO()
        elif command == 'func_with_args':
            function_name = ast[1]
            args = ast[2]
            return FunctionExecutor.execute_function(function_name, input_stream, *args)
        elif command == 'func':
            function_name = ast[1]
            return FunctionExecutor.execute_function(function_name, input_stream)
        else:
            raise KeyError(f'unknown command {command}')
