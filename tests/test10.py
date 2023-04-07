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
	print("*                     Test n°10_1                         *")
	print("* Sequence A006877                                        *")
	print("* Total stopping time records                             *")
	print("***********************************************************")
	print("")
	record_number = int(input("Number of records to generate (a value around 40 would be optimal) ? "))
	records0 = syracuse.sequences.total_stopping_time_records(0)
	records1 = syracuse.sequences.total_stopping_time_records(1)
	records2 = syracuse.sequences.total_stopping_time_records(2)
	records4 = syracuse.sequences.total_stopping_time_records(4)
	print("*** No optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records0)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration0 = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration0} seconds")
	print("*** Even numbers optimization ***")
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
	print("")
	optim = int(input("Optimization combination factor (addition of the desired optimizations) ? "))
	records_custom = syracuse.sequences.total_stopping_time_records(optim)
	print("*** custom optimization ***")
	start = time.perf_counter_ns()
	for _ in range(record_number):
		print(f"{next(records_custom)}, ", end="", flush=True)
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print("")
	print(f"Duration: {duration} seconds")
	print(f"Speedup factor against absence of optimization: {duration0/duration:.2}")

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	