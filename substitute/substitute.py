import os
import re
from typing import Optional


class Substitute():
	"""
	A module with system variables that handles substitution and assignment commands.
	"""

	def __init__(self):
		self.__env = EnvironmentHandler()

	def deref(self, command: str) -> str:
		"""
		Replaces variables names to their values in a command. Supports strong and weak quoting.
		If command is an assignment, executes it, and returns empty string.
		A variable name found in an input if '$' stays before it.
		:param command: an input command as a string
		:returns: a command with substitutions or an empty string if the command is an assignment
		:raises SubstituteException: if the input has incorrect quoting or assignment
		"""

		command = self.__substitute(command)
		assign = self.__is_assign(command)

		if assign is not None:
			var, val = assign
			self.__env.set_value(var, val)
			return ''
		else:
			return command

	def __is_assign(self, command: str) -> Optional[tuple]:
		"""
		Checks that an input command is an assignment.
		:param command: an input command as a string
		:returns: pair (variable, value) if the command is an assignment, None otherwise 
		"""

		var = r'(\w+)'
		val = r'("[^"]*"|\'[^\']*\'|[^\s\'"]+)'

		result = re.match(rf'^\s*{var}\s*=\s*{val}\s*$', command)

		if result is None or \
		   result.group(1) is None or \
		   result.group(2) is None:
			return None
		else:
			return result.group(1), self.__remove_quotes(result.group(2))

	def __remove_quotes(self, string: str) -> str:
		"""
		Removes quotes in the beggining and the end of a string if they exists.
		:param string: an input string
		:returns: a string without external quotes
		"""

		if string[0] == '"' and string[-1] == '"':
			return string[1:-1]
		elif string[0] == "'" and string[-1] == "'":
			return string[1:-1]
		else:
			return string

	def __substitute(self, string: str) -> str:
		"""
		Replaces variables names to their values in a string. Supports strong and weak quoting.
		A variable name found in an input if '$' stays before it.
		:param command: an input command as a string
		:returns: a string with substitutions
		:raises SubstituteException: if the input has incorrect quoting or assignment
		"""

		new_string = []
		open_strong = False
		open_strong_pos = None
		open_weak = False
		open_weak_pos = None
		curr_var = []

		for pos, c in enumerate(string):
			if c == "'" and not open_weak:
				open_strong = not open_strong
				if open_strong:
					open_strong_pos = pos

				if len(curr_var) == 0:
					new_string.append("'")
				elif len(curr_var) == 1:
					raise SubstituteException(pos, "Variable name can't start with quotes")
				else:
					var = ''.join(curr_var[1:])
					val = self.__env.get_value(var)
					curr_var = []
					new_string += val
					new_string.append("'")
			elif c == '"' and not open_strong:
				open_weak = not open_weak
				if open_weak:
					open_weak_pos = pos

				if len(curr_var) == 0:
					new_string.append('"')
				elif len(curr_var) == 1:
					raise SubstituteException(pos, "Variable name can't start with quotes")
				else:
					var = ''.join(curr_var[1:])
					val = self.__env.get_value(var)
					curr_var = []
					new_string += val
					new_string.append('"')
			elif c == '$' and not open_strong:
				if len(curr_var) == 0:
					curr_var.append('$')
				elif len(curr_var) == 1:
					raise SubstituteException(pos, "Variable name can't start with '$'")
				else:
					var = ''.join(curr_var[1:])
					val = self.__env.get_value(var)
					curr_var = ['$']
					new_string += val
			elif c not in [' ', '\t'] and len(curr_var) > 0:
				curr_var.append(c)
			elif c in [' ', '\t'] and len(curr_var) == 1:
				raise SubstituteException(pos, "Variable name can't be empty")
			elif c in [' ', '\t'] and len(curr_var) > 1:
				var = ''.join(curr_var[1:])
				val = self.__env.get_value(var)
				curr_var = []
				new_string += val
				new_string.append(c)
			else:
				new_string.append(c)

		if len(curr_var) == 1:
			raise SubstituteException(len(string) - 1, "Variable name can't be empty")
		elif len(curr_var) > 1:
			var = ''.join(curr_var[1:])
			val = self.__env.get_value(var)
			new_string += val

		if open_strong:
			raise SubstituteException(open_strong_pos, "Strong quoting without closing symbol")
		elif open_weak:
			raise SubstituteException(open_weak_pos, "Weak quoting without closing symbol")
		else:
			return ''.join(new_string)


class SubstituteException(Exception):
	"""
	An exception raised for errors occurred while parsing substitutuions and assignments.

	Attributes:
		pos     -- a position in input where parsing for substutute failed
		message -- a message explaining parsing failure
	"""

	def __init__(self, pos: int, message: str):
		"""
		:param pos: a position in input where parsing for substutute failed
		:param message: a message explaining parsing failure
		"""

		self.pos = pos
		self.message = message
		super().__init__(self.message)


class EnvironmentHandler():
	"""
	A module that contains system variables.
	"""

	def __init__(self):
		self.__vars = {}
		self.__vars.update(dict(os.environ))

	def set_value(self, name: str, value: str):
		"""
		Sets a new value for a variable.
		:param name: a variable's name as a string
		:param value: a new value as a string
		"""

		self.__vars[name] = value

	def get_value(self, name: str) -> str:
		"""
		Returns variable's value.
		:param name: a variable's name as a string
		:returns: a variable's value as a string if it exists, an empty string if not
		"""

		return self.__vars.get(name, '')
