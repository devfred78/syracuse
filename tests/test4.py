import itertools
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

TEST1_FILENAME_ROOT = "graph_compressed_syracuse_"
TEST2_FILENAME_ROOT = "graph_normal_syracuse_"
TEST1_TEMP_DOT_FILENAME = "compressed_temp_dot_file.dot"
TEST2_TEMP_DOT_FILENAME = "normal_temp_dot_file.dot"
PNG_FOLDER = pathlib.Path(__file__).resolve().parent / pathlib.Path("png")
TEMP_FOLDER = pathlib.Path(__file__).resolve().parent / pathlib.Path("temp")

GRAPHVIZ_PATH = pathlib.Path("C:/Program Files/Graphviz/bin")

# Main function
#--------------
def main():
	""" Main program execution"""
	
	global PNG_FOLDER
	global TEMP_FOLDER
	
	if not PNG_FOLDER.is_dir():
		if not PNG_FOLDER.exists():
			PNG_FOLDER.mkdir()
		else:
			for i in itertools.count():
				PNG_FOLDER = PNG_FOLDER.with_stem(PNG_FOLDER.stem + str(i))
				if not PNG_FOLDER.exists():
					PNG_FOLDER.mkdir()
					break
	
	if not TEMP_FOLDER.is_dir():
		if not TEMP_FOLDER.exists():
			TEMP_FOLDER.mkdir()
		else:
			for i in itertools.count():
				TEMP_FOLDER = TEMP_FOLDER.with_stem(TEMP_FOLDER.stem + str(i))
				if not TEMP_FOLDER.exists():
					TEMP_FOLDER.mkdir()
					break
					
	print("***********************************************************")
	print("*                     Test n°1                            *")
	print("* Generation of cumulative PNG files rendering graphs     *")
	print("* for iterative **compressed** Syracuse sequences         *")
	print("*                                                         *")
	print("* Usage of Graphviz, located at:                          *")
	print(f"* {str(GRAPHVIZ_PATH)}                           *")
	print("*                                                         *")
	print("* PNG files created in the following folder:              *")
	print(f"* {str(PNG_FOLDER)}                          *")
	print("***********************************************************")
	test1_syr_value = input("Highest rank of the compressed Syracuse sequences group (>= 1) ? ")
	exclude = input("Witch rank do you want to exclude ? ")
	if exclude:
		excludes = [int(exclude)]
	else:
		excludes = []
	dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
	for rank in range(1, int(test1_syr_value)+1):
		dot_out = syracuse.drawing.range_sequences_to_dot_string(compressed = True, limit=rank, orientation="landscape", excludes = excludes, colored = False)
		dot_file = TEMP_FOLDER / pathlib.Path(TEST1_TEMP_DOT_FILENAME)
		dot_file.write_text(dot_out)
		png_out = subprocess.run([dot_exe.as_posix(), "-Tpng", dot_file.as_posix()], capture_output=True, text=False).stdout
		png_file = PNG_FOLDER / pathlib.Path(TEST1_FILENAME_ROOT + str(rank) + ".png")
		png_file.write_bytes(png_out)
	
	print("")
	
	print("***********************************************************")
	print("*                     Test n°2                            *")
	print("* Generation of cumulative PNG files rendering graphs     *")
	print("* for iterative **normal** Syracuse sequences             *")
	print("*                                                         *")
	print("* Usage of Graphviz, located at:                          *")
	print(f"* {str(GRAPHVIZ_PATH)}                           *")
	print("*                                                         *")
	print("* PNG files created in the following folder:              *")
	print(f"* {str(PNG_FOLDER)}                          *")
	print("***********************************************************")
	test2_syr_value = input("Highest rank of the normal Syracuse sequences group (>= 1) ? ")
	exclude = input("Witch rank do you want to exclude ? ")
	if exclude:
		excludes = [int(exclude)]
	else:
		excludes = []
	dot_exe = GRAPHVIZ_PATH.resolve() / pathlib.Path("dot.exe")
	for rank in range(1, int(test2_syr_value)+1):
		dot_out = syracuse.drawing.range_sequences_to_dot_string(compressed = False, limit=rank, orientation="landscape", excludes = excludes, colored = False)
		dot_file = TEMP_FOLDER / pathlib.Path(TEST2_TEMP_DOT_FILENAME)
		dot_file.write_text(dot_out)
		png_out = subprocess.run([dot_exe.as_posix(), "-Tpng", dot_file.as_posix()], capture_output=True, text=False).stdout
		png_file = PNG_FOLDER / pathlib.Path(TEST2_FILENAME_ROOT + str(rank) + ".png")
		png_file.write_bytes(png_out)

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	