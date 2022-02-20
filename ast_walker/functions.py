from ast_walker.holder import FunctionHolder
from ast_walker.grep import grep
from io import BytesIO, StringIO
from os import getcwd
import contextlib


# функция-аналог bash-функции `cat` [FILE]
# выводит на экран содержимое файла
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


# функция-аналог bash-функции `echo`
# выводит на экран свой аргумент (или аргументы)
@FunctionHolder.shell_function('echo')
def echo(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(b' '.join(map(str.encode, args)))
    out.write(b' '.join(input_stream.getvalue().split()))

    return returncode, out, err


# функция-аналог bash-функции `wc` [FILE]
# выводит количество строк, слов и байт в файле
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


# функция-аналог bash-функции `pwd`
# печатает текущую директорию
@FunctionHolder.shell_function('pwd')
def pwd(input_stream, *args):
    returncode = 0
    out = BytesIO()
    err = BytesIO()

    out.write(getcwd().encode())

    return returncode, out, err


# функция-аналог bash-функции `exit`
# совершает выход из интерпретатора
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
            grep(input_stream, args)
        except:
            returncode = 1

    out.write(out_str.getvalue().encode())
    err.write(err_str.getvalue().encode())

    return returncode, out, err
