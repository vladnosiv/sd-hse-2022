import os
from pathlib import Path
import copy
import re
from typing import Optional


class EnvironmentHandler:
	"""
	A module that contains system variables.
	"""
	__vars = copy.deepcopy(dict(os.environ))
	__current_directory = Path.cwd().resolve()

	@classmethod
	def set_value(cls, name: str, value: str):
		"""
		Sets a new value for a variable.
		:param name: a variable's name as a string
		:param value: a new value as a string
		"""

		cls.__vars[name] = value

	@classmethod
	def get_value(cls, name: str) -> str:
		"""
		Returns variable's value.
		:param name: a variable's name as a string
		:returns: a variable's value as a string if it exists, an empty string if not
		"""

		return cls.__vars.get(name, '')

	@classmethod
	def resolve_path(cls, path: str) -> Path:
		"""
		Returns absolute path from `path`
		:param path: a system path
		:returns: an absolute path 
		"""
		p = Path(path)
		return p if p.is_absolute() else Path(os.path.abspath(cls.__current_directory.joinpath(p)))

	@classmethod
	def resolve_path_as_str(cls, path: str) -> str:
		return str(cls.resolve_path(path))

	@classmethod
	def get_current_working_directory(cls) -> Path:
		"""
		:returns: current working directory
		"""
		return cls.__current_directory

	@classmethod
	def set_current_working_directory(cls, path: Path):
		"""
		Sets current working directory. Whether the given path exists or not
		:param: new path
		"""
		cls.__current_directory = path


class Substitute():
	"""
	A module with system variables that handles substitution and assignment commands.
	"""

	def deref(self, command: str) -> str:
		"""
		Replaces variables names to their values in a command. Supports strong and weak quoting.
		A variable name found in an input if '$' stays before it.
		:param command: an input command as a string
		:returns: a command with substitutions
		:raises SubstituteException: if the input has incorrect quoting or '$' usage
		"""

		string = command
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
					val = EnvironmentHandler.get_value(var)
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
					val = EnvironmentHandler.get_value(var)
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
					val = EnvironmentHandler.get_value(var)
					curr_var = ['$']
					new_string += val
			elif c not in [' ', '\t'] and len(curr_var) > 0:
				curr_var.append(c)
			elif c in [' ', '\t'] and len(curr_var) == 1:
				raise SubstituteException(pos, "Variable name can't be empty")
			elif c in [' ', '\t'] and len(curr_var) > 1:
				var = ''.join(curr_var[1:])
				val = EnvironmentHandler.get_value(var)
				curr_var = []
				new_string += val
				new_string.append(c)
			else:
				new_string.append(c)

		if len(curr_var) == 1:
			raise SubstituteException(len(string) - 1, "Variable name can't be empty")
		elif len(curr_var) > 1:
			var = ''.join(curr_var[1:])
			val = EnvironmentHandler.get_value(var)
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
