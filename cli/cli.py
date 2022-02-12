class CLI():
	"""
	A module that interacts with user.
	"""

	def read(self) -> str:
		"""
		Get a command from user.
		:returns: a command as a string
		"""

		try:
			cmd = input('> ')
		except EOFError:
			print('')
			exit()

		return cmd

	def write(self, output: str):
		"""
		Shows an output to user.
		:param output: an output to show
		"""

		if len(output) > 0:
			print(output)