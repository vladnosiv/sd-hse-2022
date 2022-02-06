import sys
sys.path.append('./src')
from io import BytesIO
from cli import CLI
from substitute import Substitute
from lexer import Lexer
from parser import CommandParser
from ast_walker import ASTWalker


class Main():
	"""
	The main module that executes user's commands.
	"""

	def __init__(self):
		self.__cli    = CLI()
		self.__subs   = Substitute()
		self.__lexer  = Lexer()
		self.__parser = CommandParser()
		self.__walker = ASTWalker()

	def run(self):
		"""
		Runs command line interpreter.
		"""

		while True:
			command = self.__cli.read()
			derefed = self.__subs.deref(command)

			tokens, unmatched = self.__lexer.tokenize(derefed)
			if len(unmatched) > 0:
				self.__on_lexer_failure(derefed, unmatched)

			ast = self.__parser.parse(tokens)
			code, out, err = self.__walker.execute(ast)
			
			self.__cli.write(err.read().decode("utf-8"))
			self.__cli.write(out.read().decode("utf-8"))
			if code != 0:
				return code

	def __on_lexer_failure(self, command: str, unparsed: str):
		"""
		Informates user that command can't be parsed.
		:param command: received command from user
		:param unparsed: a part of command that lexer failed to parse
		"""

		print("Command:")
		print(command)
		print(''.join([' ' for i in range(len(command) - len(unparsed))]), '^', sep='')
		print("Invalid syntax")
		