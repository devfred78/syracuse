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
	print("*                     Test n°8_1                          *")
	print("* Generation of a global graph for a range of sequences   *")
	print("*                                                         *")
	print("* Comparison of sequential and parallel, multiprocessing  *")
	print("* computations.                                           *")
	print("***********************************************************")
	min_initial_value = int(input("Lowest initial value for the sequences range (>= 1) ? "))
	max_initial_value = int(input("Highest initial value for the sequences range (>= Lowest initial value) ? "))
	print("")
	print("Sequential computation...", end = "", flush = True)
	start = time.perf_counter_ns()
	seq_global_graph = syracuse.Syracuse.generate_global_graph(max_initial_value=max_initial_value, min_initial_value=min_initial_value)
	end = time.perf_counter_ns()
	sequential_duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print(f"finished. Total duration of computation (in seconds): {sequential_duration}")
	yesno = input("Print the sequential global graph (y/N) ? ")
	if yesno.lower() == "y":
		print(seq_global_graph)
	for algo in range(3):
		syracuse.Syracuse.reset_global_graph()
		print("")
		print(f"Parallel algorithm {algo} computation...", end = "", flush = True)
		start = time.perf_counter_ns()
		par_global_graph = syracuse.Syracuse.generate_global_graph(max_initial_value=max_initial_value, min_initial_value=min_initial_value, parallel=True)
		end = time.perf_counter_ns()
		parallel_duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
		print(f"finished. Total duration of computation (in seconds): {parallel_duration}")
		benefit = sequential_duration/parallel_duration
		if benefit < 1:
			print(f"The parallel algorithm {algo} computation lasts {1/benefit:.5} times longer than the sequential one. It is better to use sequential computation in this context !")
		else:
			print(f"The parallel algorithm {algo} computation lasts {benefit:.5} times less time than the sequential one.")
		# yesno = input("Print the parallel global graph (y/N) ? ")
		# if yesno.lower() == "y":
			# print(par_global_graph)
		# yesno = input("Compare edges between the global graphs (y/N) ?")
		# if yesno.lower() == "y":
			# lacking_edges = [e for e in seq_global_graph.edges if e not in par_global_graph.edges]
			# print(f"Edges lacking in the parallel computation: {lacking_edges}")

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	