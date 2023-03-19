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
	print("*                     Test n°9_1                          *")
	print("* Generation of a bar graph of the distribution           *")
	print("* for a range of Syracuse sequences                       *")
	print("***********************************************************")
	min_initial_value = int(input("Lowest initial value for the sequences range (>= 1) ? "))
	max_initial_value = int(input("Highest initial value for the sequences range (>= Lowest initial value) ? "))
	fig = syracuse.drawing.range_sequences_distribution_to_matplotlib_figure(int(max_initial_value), int(min_initial_value), test = True)

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	