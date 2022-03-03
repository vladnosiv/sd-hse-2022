import sys
from io import StringIO
from main import Main
from functools import wraps


def main_test(command, expected_out=None):
	main = Main(is_testing=True)
	cmd = StringIO(command)
	sys.stdin = cmd
	out = StringIO()
	sys.stdout = out

	try:
		main.run()
	except EOFError:
		 pass # its ok

	if expected_out is not None:
		assert out.getvalue() == expected_out

	sys.stdout = sys.__stdout__
	sys.stdin = sys.__stdin__


def test_echo_noargs_empty_output():
	main_test('echo', '> > ')


def test_echo_five_args_correct_output():
	main_test('echo 1 2 3 4 5', '> 1 2 3 4 5\n> ')


def test_wrong_symbol_error_output():
	main_test('@', '> Scanning error. Illegal character \'@\'\n@\n^\n> ')


def test_wrong_grammar_error_output():
	main_test('| kek |', '> Grammar error\n> ')


def test_pipes():
	main_test('echo "123" | echo', '> > ')
	main_test('/usr/bin/echo "123" | echo', '> > ')
	main_test('printf "123" | echo', '> > ')

	main_test('echo "123" | cat', '> 123\n> ')
	main_test('/usr/bin/echo "123" | cat', '> 123\n\n> ')
	main_test('printf "123" | cat', '> 123\n> ')


def test_no_crashes():
	main_test('cat cat cat cat cat cat cat')
	main_test('echo echo echo echo')
	main_test('cat "README"\'.md\'')
	main_test('"e"c\'h\'o 123')
	main_test('cat ../utils/"meow file"')
	main_test('bash -c \'echo $x\'')
