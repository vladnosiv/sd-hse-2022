import sys
from io import StringIO
from main import Main


main = Main(is_testing=True)


def test_echo_noargs_empty_output():
	cmd = StringIO('echo')
	sys.stdin = cmd
	out = StringIO()
	sys.stdout = out

	try:
		main.run()
	except EOFError:
		 pass # its ok
	out.seek(0)

	assert out.read() == '> > '
	
	sys.stdout = sys.__stdout__
	sys.stdin = sys.__stdin__


def test_echo_five_args_correct_output():
	cmd = StringIO('echo 1 2 3 4 5')
	sys.stdin = cmd
	out = StringIO()
	sys.stdout = out

	try:
		main.run()
	except EOFError:
		 pass # its ok
	out.seek(0)

	assert out.read() == '> 1 2 3 4 5\n> '
		
	sys.stdout = sys.__stdout__
	sys.stdin = sys.__stdin__


def test_wrong_symbol_error_output():
	cmd = StringIO('@')
	sys.stdin = cmd
	out = StringIO()
	sys.stdout = out

	try:
		main.run()
	except EOFError:
		 pass # its ok
	out.seek(0)

	assert out.read() == '> Scanning error. Illegal character \'@\'\n@\n^\n> '
		
	sys.stdout = sys.__stdout__
	sys.stdin = sys.__stdin__


def test_wrong_grammar_error_output():
	cmd = StringIO('| kek |')
	sys.stdin = cmd
	out = StringIO()
	sys.stdout = out

	try:
		main.run()
	except EOFError:
		 pass # its ok
	out.seek(0)

	assert out.read() == '> Grammar error\n> '
		
	sys.stdout = sys.__stdout__
	sys.stdin = sys.__stdin__


def test_pipes():
	def test_pipe(command, expected):
		cmd = StringIO(command)
		sys.stdin = cmd
		out = StringIO()
		sys.stdout = out

		try:
			main.run()
		except EOFError:
			 pass # its ok

		assert out.getvalue() == expected

		sys.stdout = sys.__stdout__
		sys.stdin = sys.__stdin__

	test_pipe('echo "123" | echo', '> 123\n> ')
	test_pipe('printf "123" | echo', '> 123\n> ')
