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
    elif len(args) == 1:
        filename = args[0]
    else:
        err.write('args must contatins one filename')
        return 1, out, err

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

    out.write(b' '.join(map(str.encode, args)))
    out.write(b' '.join(input_stream.getvalue().split()))

    return returncode, out, err


@FunctionHolder.shell_function('wc')
def wc(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    if len(args) == 0:
        content = input_stream.getvalue()
    elif len(args) == 1:
        cat_code, cat_out, cat_err = cat(BytesIO(args[0].encode()))
        content = cat_out.getvalue()

        if cat_code != 0:
            return cat_code, out, cat_err
    else:
        err.write('args must contatins one filename')
        return 1, out, err

    lines_count = len(content.split(b'\n'))
    words_count = len(content.split())
    bytes_count = len(content)

    out.write(f'\t{lines_count}\t{words_count}\t{bytes_count}\t'.encode())

    return returncode, out, err


@FunctionHolder.shell_function('pwd')
def pwd(input_stream):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(getcwd().encode())

    return returncode, out, err


@FunctionHolder.shell_function('exit')
def shell_exit(input_stream):
    exit()
