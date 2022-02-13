import sys
sys.path.append('../')
from io import BytesIO
from ply.lex import LexError
from cli import CLI
from substitute import Substitute
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
			self.__cli.write('\nKeyboard interrupt')


	def __run_loop(self):
		while True:
			command = self.__get_input()
			derefed = self.__subs.deref(command)
			if derefed is None:
				self.__cli.write('Grammar error')
				continue

			try:
				ast = self.__parser.parse(derefed)
				if ast is None:
					self.__cli.write('Grammar error')
					continue
			except LexError as e:
				self.__cli.write(e.args[0])
				self.__cli.write(e.text)
				self.__cli.write('^')
				continue

			code, out, err = ASTWalker.execute(ast)

			out.seek(0)
			err.seek(0)
			self.__cli.write(err.read().decode("utf-8"))
			self.__cli.write(out.read().decode("utf-8"))


	def __get_input(self):
		if self.__testing:
			# if in testing mode, then EOF should be handled by tests
			return self.__cli.read()
		else:
			try:
				command = self.__cli.read()
			except EOFError:
				self.__cli.write('\nEOF')
				exit()
			return command


if __name__ == '__main__':
	Main().run()
