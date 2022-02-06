from ast_walker.holder import FunctionHolder
from io import BytesIO
from os import getcwd


@FunctionHolder.shell_function('cat')
def cat(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    if len(args) == 0:
        filename = input_stream.getvalue().decode()
    else:
        filename = args[0]

    try:
        with open(filename, 'r') as file:
            out.write(file.read().encode())
    except FileNotFoundError:
        err.write(f'file {filename} does not found'.encode())
        returncode = 1
    except Exception:
        err.write('something went wrong'.encode())
        returncode = 1

    return returncode, out, err


@FunctionHolder.shell_function('echo')
def echo(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    if len(args) == 0:
        out.write(' '.join(input_stream.getvalue().split()).encode())
    else:
        out.write(' '.join(args).encode())

    return returncode, out, err


@FunctionHolder.shell_function('wc')
def wc(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    if len(args) == 0:
        content = input_stream.getvalue()
    else:
        content = args[0]

    lines_count = len(content.split(b'\n'))
    words_count = len(content.split())
    bytes_count = len(content)

    out.write(f'\t{lines_count}\t{words_count}\t{bytes_count}\t'.encode())

    return returncode, out, err


@FunctionHolder.shell_function('pwd')
def pwd(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(getcwd().encode())

    return returncode, out, err


@FunctionHolder.shell_function('exit')
def shell_exit(input_stream, *args):
    exit()
