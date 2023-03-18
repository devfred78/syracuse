"""This module provides several functions to render Collatz sequences into various displaying formats"""

import io
import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from syracuse import Syracuse, CompressedSyracuse

def single_sequence_to_dot_string(syr_sequence:Syracuse, converter:str = "native") -> str:
	"""Create a string containing a [Graphviz](https://graphviz.org/) dot format representing a single Collatz sequence, that can be read by Graphviz to render into various image formats.
	
	It is possible to choose among several "converters" to create dot strings from the Collatz sequence. The "native" one (the default) does not need any external module. It is inspirated by [https://en.wikipedia.org/wiki/File:Collatz-graph-300.svg](https://en.wikipedia.org/wiki/File:Collatz-graph-300.svg). The "pydot" one uses the `pydot` library, and creates the dot string from the internal Networkx graph.
	
	Examples:
		>>> import syracuse
		>>> import syracuse.drawing
		>>>
		>>> # Native converter
		>>> syr = syracuse.Syracuse(6)
		>>> collatz6 = syracuse.drawing.single_sequence_to_dot_string(syr)
		>>> print(collatz6)
		digraph {
		6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1;
		}
		>>>
		>>> # pydot converter
		>>> syr = syracuse.Syracuse(10)
		>>> collatz10 = syracuse.drawing.single_sequence_to_dot_string(syr, "pydot")
		>>> print(collatz10)
		strict digraph {
		10;
		5;
		16;
		8;
		4;
		2;
		1;
		10 -> 5;
		5 -> 16;
		16 -> 8;
		8 -> 4;
		4 -> 2;
		2 -> 1;
		}
	
	Parameters:
		syr_sequence:
			Sequence to be rendered
		converter:
			The converter used to create the dot string. The available values are: "native" or "pydot"
	
	Returns:
		A Graphviz dot format representation of the sequence graph
	"""
	if not isinstance(syr_sequence, Syracuse):
		raise ValueError("`syr_sequence` must be a Syracuse object")
	else:
		if converter.lower() == "pydot":
			output_str = nx.nx_pydot.to_pydot(syr_sequence.graph).to_string()
		else:
			output = io.StringIO()
			output.write("digraph {\n")
			for node in syr_sequence:
				if node == 1:
					break
				else:
					output.write(str(node) + " -> ")
			output.write("1;\n}\n")
			output_str = output.getvalue()
			output.close()
		return output_str

def range_sequences_to_dot_string(compressed:bool = False, limit:int = 10, orientation:str = "portrait", excludes:list[int] = [], colored:bool = False, converter:str = "native") -> str:
	"""Create a string containing a [Graphviz](https://graphviz.org/) dot format representing a range of Collatz sequences, that can be read by Graphviz to render into various image formats.
	
	It is possible to choose among several "converters" to create dot strings from the Collatz sequence. The "native" one (the default) does not need any external module. It is inspirated by [https://en.wikipedia.org/wiki/File:Collatz-graph-300.svg](https://en.wikipedia.org/wiki/File:Collatz-graph-300.svg). The "pydot" one uses the `pydot` library, and creates the dot string from the Networkx global graph.
	
	Examples:
		>>> import syracuse
		>>> import syracuse.drawing
		>>> collatz_range15 = syracuse.drawing.range_sequences_to_dot_string(limit = 15)
		>>> print(collatz_range15)
		digraph {
		1;
		2 -> 1;
		3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2;
		4;
		5;
		6 -> 3;
		7 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10;
		8;
		9 -> 28 -> 14 -> 7;
		10;
		11;
		12 -> 6;
		13;
		14;
		15 -> 46 -> 23 -> 70 -> 35 -> 106 -> 53 -> 160 -> 80 -> 40;
		}
		>>> collatz_range10_horizontal_colored = syracuse.drawing.range_sequences_to_dot_string(orientation = "landscape", colored = True)
		>>> print(collatz_range10_horizontal_colored)
		digraph {
		node [colorscheme=spectral10]
		1 [color=1]
		2 [color=1]
		3 [color=1]
		10 [color=3]
		5 [color=2]
		16 [color=4]
		8 [color=2]
		4 [color=1]
		6 [color=2]
		7 [color=2]
		22 [color=5]
		11 [color=3]
		34 [color=7]
		17 [color=4]
		52 [color=10]
		26 [color=6]
		13 [color=3]
		40 [color=9]
		20 [color=5]
		9 [color=2]
		28 [color=6]
		14 [color=3]
		rankdir="LR"
		1;
		2 -> 1;
		3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2;
		4;
		5;
		6 -> 3;
		7 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10;
		8;
		9 -> 28 -> 14 -> 7;
		10;
		}
	
	Parameters:
		compressed:
			indicates weither one deals with either compressed or "normal" sequences
		limit:
			the upper bound of the range values from whom the sequences are generated
		orientation:
			orientation of the rendered graph. Possible values: `landscape` or `portrait`
		excludes:
			list of sequences excluded in the range. No effect for members greater than `limit`.
		colored:
			If `True`, the rendered graph will have gradient colors, depending on the value of each node
		converter:
			The converter used to create the dot string. The available values are: "native" or "pydot". Please notice that this parameter is only relevant if colored is `False` (if colored is `True`, the native converter is used).
	
	Returns:
		A Graphviz dot format representation of the sequences range graph
	"""
	if not isinstance(limit, int):
		raise TypeError("`limit` must be an integer")
	else:
		if converter.lower() == "pydot" and not colored:
			output_str = nx.nx_pydot.to_pydot(Syracuse.generate_global_graph(max_initial_value=limit, min_initial_value=1, excludes=excludes)).to_string()
		else:
			output = io.StringIO()
			output.write("digraph {\n")
			max_all = 1
			seq_range = [seq_start for seq_start in range(1, limit+1) if seq_start not in excludes]
			if colored:
				explored = set([1])
				output.write("node [colorscheme=spectral10]\n")
				min_color_range = 1
				max_color_range = 10
				max_list = []
				for n in seq_range:
					max_list.append(CompressedSyracuse(n).max if compressed else Syracuse(n).max)
				max_all = max(max_list)
				output.write(f"1 [color={min_color_range}]\n")
				for n in seq_range:
					syr_seq = CompressedSyracuse(n) if compressed else Syracuse(n)
					for node in syr_seq:
						if node in explored:
							break
						else:
							if node == max_all:
								output.write(str(max_all) + f"[color={max_color_range}]\n")
							else:
								output.write(str(node) + f" [color={node//(max_all//max_color_range)+1}]" + "\n")
							explored.add(node)
			if orientation.lower() == "landscape":
				output.write('rankdir="LR"\n')
			explored = set([1])
			for n in seq_range:
				syr_seq = CompressedSyracuse(n) if compressed else Syracuse(n)
				for node in syr_seq:
					if node in explored:
						output.write(str(node) + ";\n")
						break
					else:
						output.write(str(node) + " -> ")
						explored.add(node)
			output.write("}\n")
			output_str = output.getvalue()
			output.close()
		return output_str

def single_sequence_to_matplotlib_figure(syr_sequence:Syracuse, test:bool = False) -> mpl.figure.Figure:
	"""Create a [Matplotlib](https://matplotlib.org/) Figure object representing the evolution of the successive values of a particular Collatz sequence.
	
	Parameters:
		syr_sequence:
			Sequence to be rendered
		test:
			if `True`, displays the graph immediately (for testing purposes)
	
	Returns:
		matplotlib.figure.Figure: A representation of the successive values of the Collatz sequence
	"""
	if not isinstance(syr_sequence, Syracuse):
		raise ValueError("`syr_sequence` must be a Syracuse object")
	else:
		fig, ax = plt.subplots()
		ax.plot(syr_sequence.total_stopping_sequence)
		ax.set_title(f"Syracuse sequence of {syr_sequence.initial_value}")
		ax.annotate(f"Total stopping time: {syr_sequence.total_stopping_time}",
					xy=(syr_sequence.total_stopping_time,1), xycoords='data',
					xytext=(-15,25), textcoords="offset points",
					arrowprops=dict(facecolor='black', shrink=0.05),
					horizontalalignment='right', verticalalignment='bottom')
		ax.annotate(f"Max value: {syr_sequence.max}",
					xy=(syr_sequence.max_rank,syr_sequence.max), xycoords='data',
					xytext=(25,-15), textcoords="offset points",
					arrowprops=dict(facecolor='black', shrink=0.05),
					horizontalalignment='left', verticalalignment='top')
		
		# Only for debug !
		if test:
			plt.show() # Display the graph
		
		return fig

def range_sequences_distribution_to_matplotlib_figure(max_initial_value:int, min_initial_value:int = 1, test:bool = False) -> mpl.figure.Figure:
	"""Create a [Matplotlib](https://matplotlib.org/) Figure object representing the distribution of the successive values of a range of Collatz sequences.
	
	Parameters:
		min_initial_value:
			The minimal initial value of the proceeded sequences
		max_initial_value:
			The maximal initial value of the proceeded sequences
		test:
			if `True`, displays the graph immediately (for testing purposes)
	
	Returns:
		matplotlib.figure.Figure: A representation of the successive values of the Collatz sequence
	
	Raises:
		ValueError:
			Raises if `min_initial_value` or `max_initial_value` are not strictly positive integers, or if `max_initial_value` < `min_initial_value`.
	"""
	if not isinstance(max_initial_value, int) or (max_initial_value <= 0):
			raise ValueError("max_initial_value must be a strictly positive integer")
	elif not isinstance(min_initial_value, int) or (min_initial_value <= 0):
		raise ValueError("min_initial_value must be a strictly positive integer")
	elif max_initial_value < min_initial_value:
		raise ValueError("max_initial_value must be greater than min_initial_value")
	else:
		x = range(min_initial_value, max_initial_value+1)
		population = dict()
		for initial_value in x:
			for value in Syracuse(initial_value, populate_global_graph = True).total_stopping_sequence:
				if value in population:
					population[value] += 1
				else:
					population[value] = 1
		y = [population[value] for value in x]
		# The max rank is obviously always 1 when min_initial_value == 1!
		if min_initial_value != 1:
			max_rank = y.index(max(y)) + min_initial_value
		
		fig, ax = plt.subplots()
		ax.bar(x, y, width=1, linewidth=0)
		ax.set_title(f"Distribution of the Syracuse({min_initial_value})-Syracuse({max_initial_value}) sequences")
		if min_initial_value != 1:
			ax.annotate(f"Max value {max(y)} reached at rank {max_rank}",
						xy=(max_rank,max(y)), xycoords='data',
						xytext=(25,-15), textcoords="offset points",
						arrowprops=dict(facecolor='black', shrink=0.05),
						horizontalalignment='left', verticalalignment='top')
		
		# Only for debug !
		if test:
			plt.show() # Display the graph
		
		return fig
		
	