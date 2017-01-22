import pizza
import slice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse

DEFAULT_INPUT_FILE = 'example.in'
OUTPUT_PLOT_FILE = 'pizza.png'
OUTPUT_FILE = 'out.txt'

def _setup_args_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--inputfile", help="the path of the inputfile containing the pizza representaion", 
		default=DEFAULT_INPUT_FILE)

	return parser.parse_args()

def _get_pizza_object(input_file):
	""" Reads input file and create pizza object. """

	with open(input_file, 'r') as input_file:
		input_string = input_file.read()

	return pizza.Pizza(input_string)


def _place_slices(pizza_object):
	""" Creates a set of slices. Loops through all tiles and create a slice (if possible) starting at that tile (i.e 
		with that tile as the top left corner of the slice). """

	# create object representing what tiles have been included in a slice
	occupied_tiles = np.zeros((pizza_object.get_height(), pizza_object.get_width()), dtype=bool)

	# define the form of the slice we'll try to fit on the pizza
	slice_width = 1
	slice_height = pizza_object.get_max_cells_per_slice()

	# loop through all tiles
	slices = []
	for row in range(pizza_object.get_height()):
		for col in range(pizza_object.get_width()):

			# create a slice starting at this tile if possible
			if _is_slice_valid(row, col, slice_width, slice_height, pizza_object, occupied_tiles):

				# mark the tiles included in this slice as "occupied"
				_mark_slice_tiles_occupied(row, col, slice_width, slice_height, occupied_tiles)

				# save slice
				slices.append(slice.Slice(row, row + slice_height-1, col, col + slice_width-1))
	
	return slices


def _is_slice_valid(start_row, start_col, slice_width, slice_height, pizza_object, occupied_tiles):
	""" Check if we can put a slice with its top-left corner at the given start coordinate. Returns True if we can do
	this and False if not. """

	tomato_count = 0
	mushroom_count = 0

	# loop through the tiles of this slice and count the number of tomatoes and mushrooms
	for i in range(start_row, start_row+slice_height):
		
		# if this slice is outside the bottom row of the pizza, it is invalid
		if i >= pizza_object.get_height():
			return False
			
		for j in range(start_col, start_col+slice_width):
			
			# if this slice is outside the rightmost column of the pizza, it is invalid
			if j >= pizza_object.get_width():
				return False

			# if this tile is already included in a slice, we cannot include it in this slice
			if occupied_tiles[i][j]:
				return False

			# count ingredient
			elif pizza_object.get_pizza()[i][j] == 'T':
				tomato_count += 1
			elif pizza_object.get_pizza()[i][j] == 'M':
				mushroom_count += 1

	return (tomato_count >= pizza_object.get_nr_each_ingredient_per_slice() and 
			mushroom_count >= pizza_object.get_nr_each_ingredient_per_slice())


def _mark_slice_tiles_occupied(start_row, start_col, slice_width, slice_heigth, occupied_tiles):
	""" Mark all the tiles in the slice with the top left corner in the given start coordinate as occupied. """

	for i in range(start_row, start_row+slice_heigth):
		for j in range(start_col, start_col+slice_width):
			occupied_tiles[i][j] = True


def _plot_result(slice_list, pizza_object):
	""" Plots a set of slices on a pizza. """

	fig = plt.figure()
	ax = fig.add_subplot(111, aspect='equal')

	# Plot axes. Y-axis is plotted "downwards". X-axis is plotted on top.
	ax.set_xlim([0, pizza_object.get_width() + 1])
	ax.xaxis.tick_top()
	ax.set_ylim([pizza_object.get_height() + 1, 0])

	# plot pizza
	ax.add_patch(patches.Rectangle((0, 0), pizza_object.get_width(), pizza_object.get_height(), 
		fill=False, linewidth=2))

	# plot ingredients
	tomatoe_coordinates = []
	mushrooms_coordinates = []
	for i in range(pizza_object.get_width()):
		for j in range(pizza_object.get_height()):
			if pizza_object.get_pizza()[j][i] == 'T':
				tomatoe_coordinates.append((i, j))
			elif pizza_object.get_pizza()[j][i] == 'M':
				mushrooms_coordinates.append((i, j))

	tomatoe_coordinates = [(e[0]+0.5, e[1]+0.5) for e in tomatoe_coordinates]
	tomatoes = ax.scatter(*zip(*tomatoe_coordinates), color='r', marker='^')
	mushrooms_coordinates = [(e[0]+0.5, e[1]+0.5) for e in mushrooms_coordinates]
	mushrooms = ax.scatter(*zip(*mushrooms_coordinates), color='b')

	# plot legend
	fig.legend((tomatoes, mushrooms), ('Tomato', 'Mushroom'), loc='lower right')

	#plot pieces
	for slice in slice_list:
		slice_width = slice.get_end_col() - slice.get_start_col() 
		slice_height = slice.get_end_row() - slice.get_start_row()
		ax.add_patch(patches.Rectangle((slice.get_start_col(), slice.get_start_row()), 
			slice_width + 1, slice_height + 1, fill=False))
	
	fig.savefig(OUTPUT_PLOT_FILE)


def _print_result_to_file(slice_list):
	""" Print slices to a file. """

	with open(OUTPUT_FILE, 'w') as output_file:
		output_file.write(str(len(slice_list)) + '\n')
		for slice in slice_list:
			output_file.write(str(slice) + '\n')


def main():
	args = _setup_args_parser()
	pizza_object = _get_pizza_object(args.inputfile)
	print('Pizza: ingredients: {}, size: {}'.format(
		pizza_object.get_nr_each_ingredient_per_slice(), pizza_object.get_max_cells_per_slice()))
	slices = _place_slices(pizza_object)
	print('Nr slices: {}'.format(len(slices)))
	_plot_result(slices, pizza_object)
	_print_result_to_file(slices)


if __name__ == "__main__":
    main()