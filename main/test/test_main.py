import sys
from io import StringIO
from main import Main
from functools import wraps
from tempfile import TemporaryDirectory
import os


def main_test(command, expected_out=None):
    main = Main(is_testing=True)
    cmd = StringIO(command)
    sys.stdin = cmd
    out = StringIO()
    sys.stdout = out

    try:
        main.run()
    except EOFError:
        pass  # its ok

    if expected_out is not None:
        assert out.getvalue() == expected_out

    sys.stdout = sys.__stdout__
    sys.stdin = sys.__stdin__


def test_echo_noargs_empty_output():
    main_test('echo', '> \n> ')


def test_echo_five_args_correct_output():
    main_test('echo 1 2 3 4 5', '> 1 2 3 4 5\n> ')


def test_wrong_symbol_error_output():
    main_test('@', '> Scanning error. Illegal character \'@\'\n> ')


def test_wrong_grammar_error_output():
    main_test('| kek |', '> Pipe\'s left command can\'t be empty\n> ')


def test_simple():
    main_test('echo "$"', '> Variable name can\'t start with quotes\n> ')
    main_test('echo 123', '> 123\n> ')
    main_test('echo "12"3', '> 123\n> ')
    main_test('echo \'$x\'', '> $x\n> ')
    main_test('echo \'$env\'var', '> $envvar\n> ')
    main_test('echo \'$env\'v\'a\'r', '> $envvar\n> ')
    main_test('echo \'$e\'n\'v\'v\'a\'r', '> $envvar\n> ')
    main_test('echo 1 2 3', '> 1 2 3\n> ')
    main_test('\'echo\' 1 2 3', '> 1 2 3\n> ')
    main_test('\'e\'c"ho" 1 2 3', '> 1 2 3\n> ')
    main_test('echo 1    2    3', '> 1 2 3\n> ')
    main_test('wc', '> \t0\t0\t0\t\n> ')
    main_test('wc', '> \t0\t0\t0\t\n> ')


def test_pipes():
    main_test('echo "123" | echo', '> \n> ')
    main_test('/usr/bin/echo "123" | echo', '> \n> ')
    main_test('printf "123" | echo', '> \n> ')

    main_test('echo "123" | cat', '> 123\n> ')
    main_test('echo "123" 456 | cat', '> 123 456\n> ')

    main_test('/usr/bin/echo "123" | cat', '> 123\n> ')
    main_test('printf "123" | cat', '> 123> ')
    main_test('echo 123 | wc', '> \t1\t1\t4\t\n> ')


def test_no_crashes():
    main_test('cat cat cat')
    main_test('echo echo echo echo')
    main_test('cat "README"\'.md\'')
    main_test('"e"c\'h\'o 123')
    main_test('cat ../utils/"meow file"')
    main_test('bash -c \'echo $x\'')


def test_check_values():
    main_test('echo echo echo echo', '> echo echo echo\n> ')
    main_test('"e"c\'h\'o 123', '> 123\n> ')


def test_env():
    main_test('x=5\nbash -c "echo $x"', '> > 5\n> ')
    main_test('x=5\nbash -c "echo $x"123', '> > 5123\n> ')
    main_test('x=5\nbash -c "echo $x"1\'2\'3', '> > 5123\n> ')
    main_test('x=5\nbash -c "echo $x"1"2"3', '> > 5123\n> ')
    main_test('x=5\nbash -c \'echo $x\'', '> > 5\n> ')
    main_test('x=5\nbash -c \"echo \'$x\'\"', '> > 5\n> ')
    main_test('x=5\nbash -c \"echo \'"$x"\'\"', '> > 5\n> ')
    main_test('x=ec\ny=ho\nbash -c \"$x$y \'"$x"\'\"', '> > > ec\n> ')
    main_test('x=ec\ny=ho\n$x$y 123', '> > > 123\n> ')
    main_test('x=ch\ne$x"o" 123', '> > 123\n> ')
    main_test('x=228\ny=$x\nx=322\necho $x$y', '> > > > 322228\n> ')
    main_test('x=echo\ny=" 1   2    3"\n$x$y', '> > > 1 2 3\n> ')
    main_test('x=ec\ny="ho 1   2    3"\n$x$y', '> > > 1 2 3\n> ')
    main_test('x======5\n', '> Wrong assignment usage\n> ')


def test_spaces_in_names():
    with TemporaryDirectory(dir='/tmp', prefix='python_shell_test') as d:
        spaced_name = 'a bc d'
        content = 'strange\nfile\ncontent'
        with open(os.path.join(d, spaced_name), 'w') as f:
            f.write(content)

        def get_path(spaced_name_case):
            return os.path.join(d, spaced_name_case)

        main_test('cat {filename}'.format(filename=get_path('\"a bc d\"')), f'> {content}> ')
        main_test('cat {filename}'.format(filename=get_path('\"a b\"\"c d\"')), f'> {content}> ')


def test_valid_stdout_and_stderr():
    with TemporaryDirectory(dir='/tmp', prefix='python_shell_test') as d:
        filepath = os.path.join(d, 'run.py')
        with open(filepath, 'w') as f:
            f.write('import sys; print("my stdout"); print("my stderr", file=sys.stderr)')

        main_test(f'python3 {filepath} | echo 123', '> my stderr\n123\n> ')
        main_test(f'python3 {filepath} | cat', '> my stderr\nmy stdout\n> ')

        # main_test(f'python3 {filepath}', '> my stdout\nmy stderr\n> ')
