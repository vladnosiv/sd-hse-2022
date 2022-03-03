from ast_walker.holder import FunctionHolder
from io import BytesIO
import subprocess
from environment import EnvironmentHandler


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
                result = subprocess.run(
                    [name] + list(args),
                    input=input_stream.getvalue(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=EnvironmentHandler.as_dict()
                )

                return result.returncode, BytesIO(result.stdout), BytesIO(result.stderr)
            except Exception as e:
                return 1, BytesIO(), BytesIO(f'{e}'.encode())
        else:
            return function(input_stream, *args)
