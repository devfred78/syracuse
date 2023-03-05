import os
import pathlib
import subprocess
import sys
import time

if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
	import syracuse
	import syracuse.drawing
else:
	from .. import syracuse
	from ..syracuse import drawing

# Main function
#--------------
def main():
	""" Main program execution"""
	
	print("***********************************************************")
	print("*                     Test n°1                            *")
	print("* Generation of a graph with the successive values        *")
	print("* for one Syracuse sequence                               *")
	print("***********************************************************")
	test1_syr_value = input("Starting value of the Syracuse sequence (>= 1) ? ")
	fig = syracuse.drawing.single_sequence_to_matplotlib_figure(syracuse.Syracuse(int(test1_syr_value)), test=True)

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	