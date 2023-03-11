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
TEST3_PYDOT_SVG_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_pydot_test7_3.svg")
TEST3_NORMAL_SVG_FILE = pathlib.Path(__file__).resolve().parent / pathlib.Path("graph_normal_test7_3.svg")
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
	print("*                     Test n°7_2                          *")
	print("* Generation of a DOT string using pydot converter        *")
	print("* for one Syracuse sequence                               *")
	print("* with optional SVG conversion by Graphviz                *")
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
	
	print("")
	
	print("***********************************************************")
	print("*                     Test n°7_3                          *")
	print("* Generation of a DOT string using normal                 *")
	print("* and pydot converter with time measurement               *")
	print("* for a range of Syracuse sequences                       *")
	print("* with optional SVG conversion by Graphviz                *")
	print("*                                                         *")
	print("***********************************************************")
	test3_syr_value = input("Highest rank of the Syracuse sequences group (>= 1) ? ")
	exclude = input("Which rank do you want to exclude ? ")
	if exclude:
		excludes = [int(exclude)]
	else:
		excludes = []
	print("Dot string generation with pydot converter...", end = "", flush = True)
	start_pydot = time.perf_counter_ns()
	dot_file = syracuse.drawing.range_sequences_to_dot_string(compressed = False, limit=int(test3_syr_value), excludes = excludes, colored = False, converter = "pydot")
	end_pydot = time.perf_counter_ns()
	pydot_duration = (end_pydot - start_pydot)/10**9 # duration in seconds, counter in nanoseconds
	print(f"finished. Total duration of generation (in seconds): {pydot_duration}")
	yesno = input("Display the generated dot string (y/N) ?")
	if yesno.lower() == "y":
		print("Generated dot file with pydot converter:")
		print(dot_file)
	yesno = input("Create a SVG file (y/N) ?")
	if yesno.lower() == "y":
		dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
		svg_out_str = subprocess.run([dot_exe.as_posix(), "-Tsvg"], input = dot_file, capture_output=True, text=True).stdout
		TEST3_PYDOT_SVG_FILE.write_text(svg_out_str)
	print("Dot string generation with normal converter...", end = "", flush = True)
	start_normal = time.perf_counter_ns()
	dot_file = syracuse.drawing.range_sequences_to_dot_string(compressed = False, limit=int(test3_syr_value), excludes = excludes, colored = False)
	end_normal = time.perf_counter_ns()
	normal_duration = (end_normal - start_normal)/10**9 # duration in seconds, counter in nanoseconds
	print(f"finished. Total duration of generation (in seconds): {normal_duration}")
	yesno = input("Display the generated dot string (y/N) ?")
	if yesno.lower() == "y":
		print("Generated dot file with normal converter:")
		print(dot_file)
	yesno = input("Create a SVG file (y/N) ?")
	if yesno.lower() == "y":
		dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
		svg_out_str = subprocess.run([dot_exe.as_posix(), "-Tsvg"], input = dot_file, capture_output=True, text=True).stdout
		TEST3_NORMAL_SVG_FILE.write_text(svg_out_str)

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	