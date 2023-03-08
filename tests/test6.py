import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import syracuse

# Main function
#--------------
def main():
	""" Main program execution"""
	
	print("***********************************************************")
	print("*                     Test n°6_1                          *")
	print("* Maximal values computation for a range of sequences     *")
	print("*                                                         *")
	print("* Comparison of sequential and parallel, multiprocessing  *")
	print("* computations.                                           *")
	print("***********************************************************")
	min_initial_value = int(input("Lowest initial value for the sequences range (>= 1) ? "))
	max_initial_value = int(input("Highest initial value for the sequences range (>= Lowest initial value) ? "))
	print("")
	print("Sequential computation...", end = "", flush = True)
	start = time.perf_counter_ns()
	max_range_tuple = syracuse.Syracuse.max_reached_values_range(max_initial_value, min_initial_value)
	end = time.perf_counter_ns()
	sequential_duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print(f"finished. Total duration of computation (in seconds): {sequential_duration}")
	print("Parallel computation...", end = "", flush = True)
	start = time.perf_counter_ns()
	max_range_tuple = syracuse.Syracuse.max_reached_values_range(max_initial_value, min_initial_value, parallel = True)
	end = time.perf_counter_ns()
	parallel_duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print(f"finished. Total duration of computation (in seconds): {parallel_duration}")
	print("")
	benefit = sequential_duration/parallel_duration
	if benefit < 1:
		print(f"The parallel computation lasts {1/benefit:.5} times longer than the sequential one. It is better to use sequential computation in this context !")
	else:
		print(f"The parallel computation lasts {benefit:.5} times less time than the sequential one.")

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	