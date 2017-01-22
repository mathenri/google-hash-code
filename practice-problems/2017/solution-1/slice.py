class Slice:
	""" Class representing a slice of pizza using four coordinats: start and end row and column. """

	def __init__(self, start_row, end_row, start_col, end_col):
		self.start_row = start_row
		self.end_row = end_row
		self.start_col = start_col
		self.end_col = end_col

	def get_start_row(self):
		return self.start_row

	def get_end_row(self):
		return self.end_row

	def get_start_col(self):
		return self.start_col

	def get_end_col(self):
		return self.end_col

	def __str__(self):
		return '{} {} {} {}'.format(self.start_row, self.start_col, self.end_row, self.end_col)