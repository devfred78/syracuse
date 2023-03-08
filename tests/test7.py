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

TEST2_SVG_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_test7_2.svg")
GRAPHVIZ_PATH = pathlib.Path("C:/Program Files/Graphviz/bin")

# Main function
#--------------
def main():
	""" Main program execution"""
	
	print("***********************************************************")
	print("*                     Test n°7_1                          *")
	print("* Generation of a DOT string using native converter       *")
	print("* for one Syracuse sequence                               *")
	print("*                                                         *")
	print("***********************************************************")
	seq_type = input("Normal or compressed Syracuse sequence (N/c) ? ")
	test1_syr_value = input("Starting value of the Syracuse sequence (>= 1) ? ")
	dot_file = syracuse.drawing.single_sequence_to_dot_string(syracuse.CompressedSyracuse(int(test1_syr_value)) if seq_type.upper() == "C" else syracuse.Syracuse(int(test1_syr_value)))
	print("Generated dot file with native converter:")
	print(dot_file)
	
	print("")

	print("***********************************************************")
	print("*                     Test n°7_1                          *")
	print("* Generation of a DOT string using pydot converter        *")
	print("* for one Syracuse sequence                               *")
	print("* with optional SVG convertion by Graphviz                *")
	print("*                                                         *")
	print("***********************************************************")
	seq_type = input("Normal or compressed Syracuse sequence (N/c) ? ")
	test1_syr_value = input("Starting value of the Syracuse sequence (>= 1) ? ")
	dot_file = syracuse.drawing.single_sequence_to_dot_string(syracuse.CompressedSyracuse(int(test1_syr_value)) if seq_type.upper() == "C" else syracuse.Syracuse(int(test1_syr_value)), converter = "pydot")
	print("Generated dot file with pydot converter:")
	print(dot_file)
	yesno = input("Create a SVG file (y/N) ?")
	if yesno.lower() == "y":
		dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
		svg_out_str = subprocess.run([dot_exe.as_posix(), "-Tsvg"], input = dot_file, capture_output=True, text=True).stdout
		TEST2_SVG_FILE.write_text(svg_out_str)

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	