import os
import sys
import time

if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
	import syracuse
else:
	from .. import syracuse

TEST1_NB_ITERATIONS = 100
TEST2_NB_ITERATIONS = 100

# Main function
#--------------
def main():
	""" Main program execution"""
	
	print("***********************************************************")
	print("*                     Test n°1_1                          *")
	print(f"*{TEST1_NB_ITERATIONS} iterations of the same computations*")
	print("*  for the first Syracuse sequences WITHOUT global graph: *")
	print("* stopping time                                           *")
	print("* total stopping time                                     *")
	print("* complete sequence                                       *")
	print("* maximal value reached                                   *")
	print("* graph view                                              *")
	print("***********************************************************")
	test1_nb_sequences = input("Highest rank of the computed sequences (>= 1) ? ")
	start = time.perf_counter_ns()
	for _ in range(TEST1_NB_ITERATIONS):
		for initial_value in range(1, int(test1_nb_sequences)+1):
			syr_sequence = syracuse.Syracuse(initial=initial_value)
			syr_sequence.stopping_time
			syr_sequence.total_stopping_time
			syr_sequence.total_stopping_sequence
			syr_sequence.max
			syr_sequence.graph_view
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print(f"Total duration of computation (in seconds): {duration}")
	print("")
	
	print("***********************************************************")
	print("*                     Test n°1_2                          *")
	print(f"*{TEST2_NB_ITERATIONS} iterations of the same computations*")
	print("*  for the first Syracuse sequences WITH global graph:    *")
	print("* stopping time                                           *")
	print("* total stopping time                                     *")
	print("* complete sequence                                       *")
	print("* maximal value reached                                   *")
	print("* graph view                                              *")
	print("***********************************************************")
	test2_nb_sequences = input("Highest rank of the computed sequences (>= 1) ? ")
	start = time.perf_counter_ns()
	for _ in range(TEST2_NB_ITERATIONS):
		for initial_value in range(1, int(test2_nb_sequences)+1):
			syr_sequence = syracuse.Syracuse(initial=initial_value, populate_global_graph=True)
			syr_sequence.stopping_time
			syr_sequence.total_stopping_time
			syr_sequence.total_stopping_sequence
			syr_sequence.max
			syr_sequence.graph_view
	end = time.perf_counter_ns()
	duration = (end - start)/10**9 # duration in seconds, counter in nanoseconds
	print(f"Total duration of computation (in seconds): {duration}")
	yesno = input("Display the global graph (y/N) ? ")
	if yesno.upper() == "Y":
		print(syracuse.Syracuse.global_graph.adj)

# Main program,
# running only if the module is NOT imported (but directly executed)
#-------------------------------------------------------------------
if __name__ == '__main__':
	main()
	