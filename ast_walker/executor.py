from ast_walker.holder import FunctionHolder
from io import BytesIO
import subprocess


class FunctionExecutor:
    '''
        Executes the function passed to it with the specified parameters
    '''
    @staticmethod
    def execute_function(name, input_stream, *args):
        '''
            name: str - function name
            input_stream: BytesIO
            *args - arguments defining the behavior of the function
        '''
        function = FunctionHolder.get_function(name)

        if function is None:
            try:
                arguments = list(args) +  [input_stream.getvalue().decode()]
                arguments = ' '.join(arguments)

                result = subprocess.run([name, arguments], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return result.returncode, BytesIO(result.stdout), BytesIO(result.stderr)
            except:
                return 1, BytesIO(), BytesIO(f'{name}: command not found'.encode())
        else:
            return function(input_stream, *args)
