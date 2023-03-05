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

TEST1_SVG_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_test2_1.svg")
TEST2_SEQ_LIMIT = 15
TEST2_DOT_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_test2_2.dot")
TEST2_SVG_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_test2_2.svg")
TEST2_PNG_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_test2_2.png")
TEST3_SVG_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_test2_3.svg")
GRAPHVIZ_PATH = pathlib.Path("C:/Program Files/Graphviz/bin")

# Main function
#--------------
def main():
	""" Main program execution"""
	
	print("***********************************************************")
	print("*                     Test n°1                            *")
	print("* Generation of an SVG file rendering the graph           *")
	print("* for one Syracuse sequence                               *")
	print("*                                                         *")
	print("* Usage of Graphviz, located at:                          *")
	print(f"* {str(GRAPHVIZ_PATH)}                           *")
	print("*                                                         *")
	print("* Creation of the following SVG file:                     *")
	print(f"* {str(TEST1_SVG_FILE)}                          *")
	print("***********************************************************")
	seq_type = input("Normal or compressed Syracuse sequence (N/c) ? ")
	test1_syr_value = input("Starting value of the Syracuse sequence (>= 1) ? ")
	dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
	dot_file = syracuse.drawing.single_sequence_to_dot_string(syracuse.CompressedSyracuse(int(test1_syr_value)) if seq_type.upper() == "C" else syracuse.Syracuse(int(test1_syr_value)))
	print("Generated dot file:")
	print(dot_file)
	svg_out_str = subprocess.run([dot_exe.as_posix(), "-Tsvg"], input=dot_file, capture_output=True, text=True).stdout
	TEST1_SVG_FILE.write_text(svg_out_str)
	
	print("")
	
	print("***********************************************************")
	print("*                     Test n°2                            *")
	print("* Generation of an SVG file rendering the graph           *")
	print("* for several compressed Syracuse sequences               *")
	print("*                                                         *")
	print("* Usage of Graphviz, located at:                          *")
	print(f"* {str(GRAPHVIZ_PATH)}                           *")
	print("*                                                         *")
	print("* Creation of the following SVG file:                     *")
	print(f"* {str(TEST2_SVG_FILE)}                          *")
	print("***********************************************************")
	test2_syr_value = input("Highest rank of the compressed Syracuse sequences group (>= 1) ? ")
	exclude = input("Which rank do you want to exclude ? ")
	if exclude:
		excludes = [int(exclude)]
	else:
		excludes = []
	print(f"Rank excluded: {excludes}")
	dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
	dot_file = syracuse.drawing.range_sequences_to_dot_string(compressed = True, limit=int(test2_syr_value), orientation="landscape", excludes = excludes, colored = False)
	# print("Generated dot file:")
	# print(dot_file)
	svg_out_str = subprocess.run([dot_exe.as_posix(), "-Tsvg"], input = dot_file, capture_output=True, text=True).stdout
	TEST2_SVG_FILE.write_text(svg_out_str)
	# TEST2_DOT_FILE.write_text(dot_file)
	# png_out = subprocess.run([dot_exe.as_posix(), "-Tpng", TEST2_DOT_FILE.as_posix()], capture_output=True, text=False).stdout
	# TEST2_PNG_FILE.write_bytes(png_out)
	
	print("***********************************************************")
	print("*                     Test n°3                            *")
	print("* Generation of an SVG file rendering the graph           *")
	print("* for several Syracuse sequences                          *")
	print("*                                                         *")
	print("* Usage of Graphviz, located at:                          *")
	print(f"* {str(GRAPHVIZ_PATH)}                           *")
	print("*                                                         *")
	print("* Creation of the following SVG file:                     *")
	print(f"* {str(TEST3_SVG_FILE)}                          *")
	print("***********************************************************")
	test2_syr_value = input("Highest rank of the Syracuse sequences group (>= 1) ? ")
	exclude = input("Witch rank do you want to exclude ? ")
	if exclude:
		excludes = [int(exclude)]
	else:
		excludes = []
	print(f"Rank excluded: {excludes}")
	dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
	dot_file = syracuse.drawing.range_sequences_to_dot_string(compressed = False, limit=int(test2_syr_value), orientation="landscape", excludes = excludes, colored = False)
	# print("Generated dot file:")
	# print(dot_file)
	svg_out_str = subprocess.run([dot_exe.as_posix(), "-Tsvg"], input = dot_file, capture_output=True, text=True).stdout
	TEST3_SVG_FILE.write_text(svg_out_str)
	# TEST2_DOT_FILE.write_text(dot_file)
	# png_out = subprocess.run([dot_exe.as_posix(), "-Tpng", TEST2_DOT_FILE.as_posix()], capture_output=True, text=False).stdout
	# TEST2_PNG_FILE.write_bytes(png_out)

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	