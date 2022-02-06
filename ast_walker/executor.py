from ast_walker.holder import FunctionHolder
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
            result = subprocess.run([name, input_stream.read()], stdout=subprocess.PIPE)
            return result.returncode, result.stdout, result.stderr
        else:
            return function(input_stream, *args)
