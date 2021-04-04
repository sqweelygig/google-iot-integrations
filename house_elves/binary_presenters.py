def terminal_presenter(data):
	"""Present a binary array on a single console line"""
	output = ':'
	for datum in data:
		output += '*' if datum else ' '
	print(output)
