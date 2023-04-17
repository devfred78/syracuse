import os
import pathlib
import subprocess
import sys
import time

if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
	import syracuse
	import syracuse.drawing
	import syracuse.sequences
else:
	from .. import syracuse
	from ..syracuse import drawing
	from ..syracuse import sequences

# Main function
#--------------
def main():
	""" Main program execution"""
	
	print("***********************************************************")
	print("*                     Test n°11_1                         *")
	print("* Sequence A006884                                        *")
	print("* Max value records                                       *")
	print("***********************************************************")
	print("")
	record_number = int(input("Number of records to generate (a value around 30 would be reasonable) ? "))
	records0 = syracuse.sequences.max_value_records(0)
	records1 = syracuse.sequences.max_value_records(1)
	records2 = syracuse.sequences.max_value_records(2)
	records4 = syracuse.sequences.max_value_records(4)
	records8 = syracuse.sequences.max_value_records(8)
	print("*** No optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records0)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration0 = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration0} seconds")
	print("*** Odd numbers optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records1)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration} seconds")
	print(f"Speedup factor against absence of optimization: {duration0/duration:.2}")
	print("*** k mod 6 = 5 optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records2)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration} seconds")
	print(f"Speedup factor against absence of optimization: {duration0/duration:.2}")
	print("*** a posteriori cutoff optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records4)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration} seconds")
	print(f"Speedup factor against absence of optimization: {duration0/duration:.2}")
	print("*** make_odd optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records8)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration} seconds")
	print(f"Speedup factor against absence of optimization: {duration0/duration:.2}")
	print("")
	optim = int(input("Optimization combination factor (addition of the desired optimizations) ? "))
	records_custom = syracuse.sequences.max_value_records(optim)
	print("*** custom optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records_custom)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration} seconds")
	print(f"Speedup factor against absence of optimization: {duration0/duration:.4}")

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	