class Substitute():
	"""
	A module with system variables that can substitute values into string.
	"""

	def __init__(self):
		self.__env = EnvironmentHandler()

	def deref(self, string: str) -> str:
		"""
		Replaces variables names to their values in a string.
		A variable name found in an input if '$' stays before it.
		:param string: an input string
		:returns: a string with substitutions
		"""

		return string


class EnvironmentHandler():
	"""
	A module that contains system variables.
	"""

	def get_value(self, name: str) -> str:
		"""
		Returns variable's value.
		:param name: a variable's name as a string
		:returns: a variable's value as a string if it exists, an empty string if not
		"""

		return ''