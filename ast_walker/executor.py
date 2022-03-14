import os

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
                input_content = input_stream.getvalue().decode()
                if input_content != '':
                    arguments = list(args) + [input_content]
                else:
                    arguments = list(args)
                arguments = ' '.join(arguments)

                wd = EnvironmentHandler.get_current_working_directory()
                if arguments == '':
                    result = subprocess.run(name, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=wd)
                else:
                    result = subprocess.run([name, arguments], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=wd)

                return result.returncode, BytesIO(result.stdout), BytesIO(result.stderr)
            except:
                return 1, BytesIO(), BytesIO(f'{name}: command not found'.encode())
        else:
            return function(input_stream, *args)
