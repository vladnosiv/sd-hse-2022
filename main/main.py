import sys
sys.path.append('../')
from io import BytesIO
from ply.lex import LexError
from cli import CLI
from environment import Substitute, SubstituteException
from command_parser import CommandParser
from ast_walker import ASTWalker


class Main():
	"""
	The main module that executes user's commands.
	"""

	def __init__(self, is_testing=False):
		self.__cli     = CLI()
		self.__subs    = Substitute()
		self.__parser  = CommandParser()
		self.__testing = is_testing

	def run(self):
		"""
		Runs command line interpreter.
		"""

		try:
			return self.__run_loop()
		except KeyboardInterrupt:
			self.__cli.write('\nKeyboard interrupt\n')


	def __run_loop(self):
		while True:
			command = self.__get_input()

			try:
				derefed = self.__subs.deref(command)
			except SubstituteException as e:
				self.__cli.write(e.message + '\n')
				self.__cli.write(command + '\n')
				self.__cli.write(''.join([' ' for _ in range(e.pos)]) +'^' + '\n')
				continue

			try:
				ast = self.__parser.parse(derefed)
				if ast is None:
					self.__cli.write('Grammar error\n')
					continue
			except LexError as e:
				self.__cli.write(e.args[0] + '\n')
				self.__cli.write(e.text + '\n')
				self.__cli.write('^' + '\n')
				continue

			code, out, err = ASTWalker.execute(ast)

			if len(err.getvalue()) > 0:
				self.__cli.write(err.getvalue().decode("utf-8") + '\n')

			self.__cli.write(out.getvalue().decode("utf-8"))


	def __get_input(self):
		if self.__testing:
			# if in testing mode, then EOF should be handled by tests
			return self.__cli.read()
		else:
			try:
				command = self.__cli.read()
			except EOFError:
				self.__cli.write('\nEOF\n')
				exit()
			return command


if __name__ == '__main__':
	Main().run()
