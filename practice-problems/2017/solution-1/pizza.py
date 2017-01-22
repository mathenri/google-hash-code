class Pizza:
	""" Class representing a pizza using a matrix of tiles. """

	def __init__(self, pizza_string):
		""" Creates a pizza from a string. """

		first_line = pizza_string.split('\n', 1)[0]
		pizza_content = pizza_string.split('\n')[1:-1]

		# get pizza meta data
		first_line_tokens = first_line.split()
		self.nr_each_ingredient_per_slice = int(first_line_tokens[2])
		self.max_cells_per_slice = int(first_line_tokens[3])

		# get pizza matrix
		self.pizza = [list(row) for row in pizza_content]

	def get_nr_each_ingredient_per_slice(self):
		return self.nr_each_ingredient_per_slice

	def get_max_cells_per_slice(self):
		return self.max_cells_per_slice

	def get_pizza(self):
		return self.pizza

	def get_width(self):
		return len(self.pizza[0])

	def get_height(self):
		return len(self.pizza)

	def __str__(self):
		string = []
		string.append('Ingredients per slice: ' + self.nr_each_ingredient_per_slice)
		string.append('Max cells per slice: ' + self.max_cells_per_slice)
		string.append('\n'.join([''.join(row) for row in self.pizza]))
		return '\n'.join(string)