from ast_walker.holder import FunctionHolder
from io import BytesIO, StringIO
from os import getcwd
import contextlib


# Usage: cat [FILE]
# Prints file content, or input stream if file not specified.
@FunctionHolder.shell_function('cat')
def cat(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    if len(args) == 0:
        out.write(input_stream.getvalue())
        return returncode, out, err

    for filename in args:
        try:
            with open(filename, 'r') as file:
                out.write(file.read().encode())
        except FileNotFoundError:
            err.write(f'file {filename} does not found\n'.encode())
            returncode = 1
        except Exception:
            err.write('something went wrong\n'.encode())
            returncode = 1

    return returncode, out, err


# Usage: echo [ARGS]...
# Prints args.
@FunctionHolder.shell_function('echo')
def echo(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(b' '.join(map(str.encode, args)) + b'\n')

    return returncode, out, err


# Usage: wc [FILE]
# Prints number of lines, words and bytes in file.
@FunctionHolder.shell_function('wc')
def wc(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    def get_values(content):
        lines_count = content.count(b'\n')
        words_count = len(content.split())
        bytes_count = len(content)
        return f'\t{lines_count}\t{words_count}\t{bytes_count}\t'


    if len(args) == 0:
        content = input_stream.getvalue()
        out.write(get_values(content).encode() + b'\n')
        return returncode, out, err

    for filename in args:
        cat_code, cat_out, cat_err = cat(BytesIO(), filename)
        content = cat_out.getvalue()

        if cat_code != 0:
            returncode = cat_code
            err.write(cat_err.getvalue())

        out.write(f'{get_values(content)}{filename}\n'.encode())

    return returncode, out, err


# Usage: pwd
# Prints path to the current directory.
@FunctionHolder.shell_function('pwd')
def pwd(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(getcwd().encode())

    return returncode, out, err


# Usage: exit
# Shut down CLI.
@FunctionHolder.shell_function('exit')
def shell_exit(input_stream, *args):
    exit()
