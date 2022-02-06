import sys
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

	def __init__(self):
		self.__cli    = CLI()
		self.__subs   = Substitute()
		self.__parser = CommandParser()

	def run(self):
		"""
		Runs command line interpreter.
		"""

		while True:
			command = self.__cli.read()
			derefed = self.__subs.deref(command)

			try:
				ast = self.__parser.parse(derefed)
				if ast is None:
					self.__cli.write('Grammar error')
					continue
			except LexError as e:
				self.__cli.write(e.args)
				self.__cli.write(e.s)
				self.__cli.write('^')
				continue

			code, out, err = ASTWalker.execute(ast)

			out.seek(0)
			err.seek(0)
			self.__cli.write(err.read().decode("utf-8"))
			self.__cli.write(out.read().decode("utf-8"))

			if code != 0:
				return code

if __name__ == '__main__':
	Main().run()
