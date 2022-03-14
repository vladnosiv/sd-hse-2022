import contextlib
import os
from io import BytesIO, StringIO
from pathlib import Path

from ast_walker.grep import grep
from ast_walker.holder import FunctionHolder
from environment import EnvironmentHandler


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
    elif len(args) == 1:
        filename = EnvironmentHandler.resolve_path(args[0])
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


# Usage: echo [ARGS]...
# Prints args.
@FunctionHolder.shell_function('echo')
def echo(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(b' '.join(map(str.encode, args)))
    out.write(b' '.join(input_stream.getvalue().split()))

    return returncode, out, err


# Usage: wc [FILE]
# Prints number of lines, words and bytes in file.
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
        err.write(b'args must contatins one filename')
        return 1, out, err

    lines_count = len(content.split(b'\n'))
    words_count = len(content.split())
    bytes_count = len(content)

    out.write(f'\t{lines_count}\t{words_count}\t{bytes_count}\t'.encode())

    return returncode, out, err


# Usage: pwd
# Prints path to the current directory.
@FunctionHolder.shell_function('pwd')
def pwd(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(str(EnvironmentHandler.get_current_working_directory()).encode())

    return returncode, out, err


# Usage: exit
# Shut down CLI.
@FunctionHolder.shell_function('exit')
def shell_exit(input_stream, *args):
    exit()


# функция-аналог bash-функции `grep`
# ищет шаблон в файле/потоке
@FunctionHolder.shell_function('grep')
def shell_grep(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out_str = StringIO()
    err_str = StringIO()

    with contextlib.redirect_stdout(out_str) and contextlib.redirect_stderr(err_str):
        try:
            grep(input_stream, list(args))  # I beg you
        except:
            returncode = 1

    out.write(out_str.getvalue().encode())
    err.write(err_str.getvalue().encode())

    return returncode, out, err


# Usage: cd [DIRECTORY]
# Changes the working directory to DIRECTORY.
# If the argument was not provided, changes the working directory to the user's home directory.
@FunctionHolder.shell_function('cd')
def shell_cd(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    if len(args) == 0:
        args = [str(Path.home())]

    if len(args) == 1:
        path = EnvironmentHandler.resolve_path(args[0])
        if not os.path.isdir(path):
            msg = b'Not a directory' if os.path.exists(path) else b'No such directory found'
            err.write(msg)
            return 1, out, err
        EnvironmentHandler.set_current_working_directory(path)
        os.chdir(path)
    else:
        err.write(b'args must contain one filename')
        return 1, out, err

    return returncode, out, err


# Usage: ls [DIRECTORY]
# List DIRECTORY contents.
# If the argument was not provided, lists current working directory contents.
@FunctionHolder.shell_function('ls')
def shell_ls(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()
    if len(args) == 0:
        content = os.listdir(EnvironmentHandler.get_current_working_directory())
    elif len(args) == 1:
        path = EnvironmentHandler.resolve_path(args[0])
        if os.path.exists(path):
            if os.path.isdir(path):
                content = os.listdir(path)
            else:
                content = [path.name]
        else:
            err.write(b'Directory not found')
            return 1, out, err
    else:
        err.write(b'args must contain one filename')
        return 1, out, err
    out.write(str.encode('\n'.join(content)))
    return returncode, out, err
