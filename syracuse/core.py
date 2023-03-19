"""This module provides two classes to represent a full or a compressed form of Collatz sequence."""

import itertools
from multiprocessing import Pool, Manager, Process, Queue
import os
from typing import Tuple

import more_itertools
import networkx as nx

class Syracuse():
	"""
	A (full) Collatz sequence instanciated with a given initial value.
	
	The instance is iterable, and gives the successive values of the Collatz sequence.
	
	!!! example
	
		```python linenums="1"
		syracuse = Syracuse(1000)
		for value in syracuse:
			print(value)
			if value == 1:
				break
		```
	
	Be aware that a Collatz sequence is infinite: once it reaches 1 (and that is apparently the case for all tested initial values until now !), the cycle 4,2,1 returns indefinitely. So make sure you have implemented a stopping condition when you iterate over the sequence.
	
	For each sequence an underlying, directional graph is implemented, and is populated the first time several attributes are read (like `total_stopping_time`, `max` and of course `graph` and `graph_view`), resulting an additionnal computing duration, that can be noticeable on "big" sequences. But the duration becomes imperceptible next times those attributes are read.
	
	Furthermore, a "global" graph can be optionaly initialized, and is shared with all instances. It is basically useful when working on a large number of sequences, or on same sequences repeatedly. If a global graph population is asked for a sequence instantiation, then the local graph is deduced from it only when needed, and stored in a class attribute for further use. Be aware that the global graph activation generates a significant amount of additional memory storage, but on the other side the computation speed is generally highly improved.
	
	Parameters:
		initial:
			Initial value of the Collatz sequence. Must be strictly positive.
		populate_global_graph:
			If `True`, a global graph is built, and populated with the graph of the current sequence. Default is `False`
	
	Attributes:
		initial_value:
			Reminder of the initial value given for the sequence initialisation. **read-only**
		stopping_time:
			The smallest rank such that the value becomes lower than the initial one. **read-only**
		total_stopping_time:
			The smallest rank such that the value equals 1. **read-only**
		total_stopping_sequence:
			Tuple of the sequence from the initial value, to 1. **read-only**
		max:
			Maximum value of the sequence. **read-only**
		max_rank:
			Rank of the maximum value of the sequence. **read-only**
		graph_view:
			A dict-like structure representing the graph of the successive members of the current sequence. **read-only**
		graph (networkx.Digraph):
			The underlying, directional graph for the current Collatz sequence. **read-only**
		global_graph (networkx.Digraph):
			The global graph shared with all sequences, gathering in the same graph all sequences' graphs instanciated with `populate_global_graph = True`. **read-only**
		single_graphs (dict[networkx.Digraph]):
			Store the graphs generated for a single sequence to avoid repeated computations of the same graph (used only if `populate_global_graph` is `True`)
		
	Raises:
		ValueError:
			Raises if `initial` is not a strictly positive integer.
	"""
	
	global_graph:nx.DiGraph = nx.DiGraph()
	single_graphs:dict[nx.DiGraph] = {}
	
	
	def __init__(self, initial:int, populate_global_graph:bool = False):
		# syracuse instance initialisation
		if not isinstance(initial, int) or (initial <= 0):
			raise ValueError
		else:
			self._initial = initial
			self._stopping_time = 0
			self._graph = nx.DiGraph()
			self._local_graph_completed = False # Flag switching to True when the instance's graph is complete
			self._populate_global_graph = populate_global_graph
			if self._populate_global_graph:
				self._generate_graph()
	
	def __iter__(self):
		# The Syracuse instance is iterable, and gives the successive values of the Collatz sequence
		Un = self._initial
		yield Un # Don't forget to yield the initial value !
		while True:
			Un = Un*3+1 if Un%2 else Un//2
			yield Un
	
	@property
	def initial_value(self) -> int:
		# Reminder of the initial value given for the sequence initialisation (read-only attribute)
		return self._initial
	
	@property
	def stopping_time(self) -> int:
		# The smallest rank such that the value becomes lower than the initial one (read-only attribute)
		#
		# The Collatz conjecture asserts that this rank is finite for every initial value strictly greater than 1. Postulating this, if `initial_value` == 1, then `stopping_time` returns 0
		
		if self._stopping_time == 0:
			if self._initial == 1:
				return self._stopping_time
			else:
				for index, value in enumerate(self):
					if value < self._initial:
						self._stopping_time = index
						return self._stopping_time
						break
		else:
			return self._stopping_time

	@property
	def total_stopping_time(self) -> int:
		# The smallest rank such that the value equals 1 (read-only attribute)
		#
		# The Collatz conjecture asserts that this rank is finite for every initial value.
		
		return len(self.graph) - 1
	
	@property
	def total_stopping_sequence(self) -> Tuple[int]:
		# Tuple of the sequence from the initial value, to 1 (read-only attribute)
		return tuple(self.graph.nodes)
	
	@property
	def max(self) -> int:
		# Maximum value of the sequence (read-only attribute)
		return max(self.total_stopping_sequence)
	
	@property
	def max_rank(self) -> int:
		# Rank of the maximum value of the sequence (read-only attribute)
		return self.total_stopping_sequence.index(self.max)
	
	@property
	def graph_view(self) -> dict:
		# A dict-like structure representing the graph of the successive members of the current sequence (read-only attribute)
		return self.graph.adj
	
	@property
	def graph(self) -> nx.DiGraph:
		# The underlying, directional graph for the current Collatz sequence
		self._generate_graph()
		if self._populate_global_graph:
			if self._initial in self.single_graphs:
				return self.single_graphs[self._initial]
			else:
				self.single_graphs[self._initial] = self._graph = nx.path_graph(nx.shortest_path(self.global_graph, source=self._initial, target=1), create_using=nx.DiGraph)
				return self.single_graphs[self._initial]
		else:
			return self._graph
	
	def _generate_graph(self):
		"""Generate the internal, (directed) graph for the current sequence. Populate also the global graph if activated."""
		if not self._local_graph_completed:
			if self._populate_global_graph:
				for Un in self:
					if Un == self._initial:
						if Un in self.global_graph:
							self._local_graph_completed = True
							break
						else:
							self.global_graph.add_node(Un)
					else:
						if Un in self.global_graph:
							self.global_graph.add_edge(previous,Un)
							self._local_graph_completed = True
							break
						self.global_graph.add_edge(previous,Un)
					previous = Un
					
					if Un == 1:
						self._local_graph_completed = True
						break
			else:
				for Un in self:
					if Un == self._initial:
						self._graph.add_node(Un)
					else:
						self._graph.add_edge(previous,Un)
					previous = Un
					
					if Un == 1:
						self._local_graph_completed = True
						break
	
	
	@classmethod
	def _atomic_task_create_independent_global_graph0(cls, initials:Tuple[int]) -> nx.DiGraph:
		"""
		An elementary task executed by the workers.
		
		Here, the tasks consists of creating a global graph with the Collatz sequences beginning by the members of the `initials` tuple, WITHOUT populating the `global_graph` class property.
		
		Parameters:
			initials:
				Tuple of integers representing the initial values of the Collatz sequences building the global graph.
		
		Returns:
			networkx.DiGraph: A representation of the global graph of the Collatz sequences.
		
		Raises:
			ValueError:
				Raises if at least one member of `initials` is not a strictly positive integer.
		"""
		independent_global_graph = nx.DiGraph()
		for initial in initials:
			if not isinstance(initial, int) or initial<=0:
				raise ValueError(f"{initial} is not a strictly positive integer")
			collatz = cls(initial)
			for Un in collatz:
				if Un == collatz.initial_value:
						if Un in independent_global_graph:
							break
						else:
							independent_global_graph.add_node(Un)
				else:
					if Un in independent_global_graph:
						independent_global_graph.add_edge(previous,Un)
						break
					independent_global_graph.add_edge(previous,Un)
				previous = Un
				
				if Un == 1:
					break
		return independent_global_graph

	@classmethod
	def _atomic_task_create_independent_global_graph1(cls, initials:Tuple[int], global_edges:list[tuple], global_nodes:list[int]) -> None:
		"""
		An elementary task executed by the workers.
		
		Here, the tasks consists of creating a shared lists of edges and nodes, that will update the global graph later, with the Collatz sequences beginning by the members of the `initials` tuple, WITHOUT populating the `global_graph` class property.
		
		Parameters:
			initials:
				Tuple of integers representing the initial values of the Collatz sequences building the global graph.
			global_edges:
				Multiprocess shared list of 2-tuples representing the edges of the future global directional graph.
			global_nodes:
				Multiprocess shared list of the nodes of the future global directional graph.
		
		Raises:
			ValueError:
				Raises if at least one member of `initials` is not a strictly positive integer.
		"""
		local_edges = []
		local_nodes = []
		for initial in initials:
			if not isinstance(initial, int) or initial<=0:
				raise ValueError(f"{initial} is not a strictly positive integer")
			if initial not in global_nodes:
				collatz = cls(initial)
				for Un in collatz:
					if Un != initial:
						local_edges.append((previous,Un))
					if Un in local_nodes:
						break
					local_nodes.append(Un)
					previous = Un
					if Un == 1:
						break
		global_edges += local_edges
		global_nodes += local_nodes

	@classmethod
	def _atomic_task_create_independent_global_graph2(cls, initials:Tuple[int], queue:Queue) -> None:
		"""
		An elementary task executed by the workers.
		
		Here, the tasks consists of creating a directional graph with the Collatz sequences beginning by the members of the `initials` tuple, WITHOUT populating the `global_graph` class property, and sending the resulting graph to the parent process through the given multiprocessing.Queue.
		
		Parameters:
			initials:
				Tuple of integers representing the initial values of the Collatz sequences building the graph.
			queue (multiprocessing.Queue):
				Queue to send the list of edges to the parent process.
				
		Raises:
			ValueError:
				Raises if at least one member of `initials` is not a strictly positive integer.
		"""
		local_graph = nx.DiGraph()
		for initial in initials:
			if not isinstance(initial, int) or initial<=0:
				raise ValueError(f"{initial} is not a strictly positive integer")
			if initial not in local_graph:
				collatz = cls(initial)
				for Un in collatz:
					if Un == collatz.initial_value:
						if Un in local_graph:
							break
						else:
							local_graph.add_node(Un)
					else:
						if Un in local_graph:
							local_graph.add_edge(previous,Un)
							break
						local_graph.add_edge(previous,Un)
					previous = Un
					
					if Un == 1:
						break
		queue.put(local_graph)
	
	@classmethod
	def generate_global_graph(cls, max_initial_value:int, min_initial_value:int = 1, excludes:list[int] = [], reverse:bool = False, parallel:bool = False, parallel_algo:int = 0) -> nx.DiGraph:
		"""Generate a global graph gathering all Collatz sequences with initial values from `min_initial_value` to `max_initial_value`, without those beginning by members of `excludes`.
		
		To populate the graph, this function temporarly instanciates the needed Syracuse objects, that can cause lot of memory consumtion; nevertheless each instance are deleted before the initialization of the next one.
		The resulting graph is stored in the class attribute `global_graph`, and is returned by this function too for convenience.
		
		It is possible to switch to an alternative computation algorithm, using the ability of the computer/OS to execute simultaneous tasks. Depending on the hardware (ie: number of "cores" of the CPU), the benefit can be really interesting for a large range of values (the definition of "large" depends heavily on your configuration). For the most little ranges, it is better to use the classical, sequential approach.
		
		The available types of parallel computation are the following:
		
		| Type number | Description                                                             |
		| ----------- | ----------------------------------------------------------------------- |
		| 0           | Usage of `multiprocessing.Pool` objects.                                |
		| 1           | Usage of `multiprocessing.Process` objects: each process computes a part of edges and nodes of the global graph as shared objects, and the global graph is built in the parent process once all edges and nodes are ready.|
		| 2           | Usage of `multiprocessing.Process` objects: each process computes its own part of the global graph, and the full global graph is later gathered in the parent process. |
		
		Parameters:
			min_initial_value:
				The minimal initial value of the proceeded sequences.
			max_initial_value:
				The maximal initial value of the proceeded sequences.
			excludes:
				list of sequences excluded in the range. No effect for members lower than `min_initial_value` or greater than `max_initial_value`.
			reverse:
				If `True`, generate the global graph by computing the constitutive sequences from the maximal to the minimal initial value. Only relevant for non-parallel computation (ie: if `parallel` is `False`).
			parallel:
				If `True`, activates the parallel computation algorithm, using pool of multiprocessing workers.
			parallel_algo:
				Type of algorithm used for the parallel computation. Only relevant when `parallel` is `True`.
		
		Returns:
			networkx.DiGraph: A representation of the global graph of the Collatz sequences.
		
		Raises:
			ValueError:
				Raises if `min_initial_value` or `max_initial_value` are not strictly positive integers, or if `max_initial_value` < `min_initial_value`.
		"""
		if not isinstance(max_initial_value, int) or (max_initial_value <= 0):
			raise ValueError("max_initial_value must be a strictly positive integer")
		elif not isinstance(min_initial_value, int) or (min_initial_value <= 0):
			raise ValueError("min_initial_value must be a strictly positive integer")
		elif max_initial_value < min_initial_value:
			raise ValueError("max_initial_value must be greater than min_initial_value")
		else:
			if parallel:
				if parallel_algo == 1:
					with Manager() as manager:
						global_edges = manager.list()
						global_nodes = manager.list()
						nb_workers = os.cpu_count() - 1
						initial_list = [x for x in range(min_initial_value, max_initial_value+1) if x not in excludes]
						distribution = [tuple(chunk) for chunk in more_itertools.distribute(nb_workers,initial_list)] # Usage of more_itertools.distribute() because the order of elements in a chunk is unimportant
						workers = []
						for chunk in distribution:
							workers.append(Process(target=cls._atomic_task_create_independent_global_graph1, args=(chunk,global_edges,global_nodes)))
						for worker in workers:
							worker.start()
						for worker in workers:
							worker.join()
						cls.global_graph.update(edges=global_edges)

				elif parallel_algo == 2:
					with Manager() as manager:
						nb_workers = os.cpu_count()
						initial_list = [x for x in range(min_initial_value, max_initial_value+1) if x not in excludes]
						distribution = [tuple(chunk) for chunk in more_itertools.distribute(nb_workers,initial_list)] # Usage of more_itertools.distribute() because the order of elements in a chunk is unimportant
						workers = []
						queue = manager.Queue()
						for chunk in distribution:
							workers.append(Process(target=cls._atomic_task_create_independent_global_graph2, args=(chunk,queue)))
						for worker in workers:
							worker.start()
						for index, _ in enumerate(range(nb_workers)):
							graph = queue.get()
							cls.global_graph.update(graph)
				
				else:
					with Pool() as pool: # Number of worker processes: os.cpu_count() (default)
						initial_list = [x for x in range(min_initial_value, max_initial_value+1) if x not in excludes]
						distribution = [tuple(chunk) for chunk in more_itertools.distribute(os.cpu_count(),initial_list)] # Usage of more_itertools.distribute() because the order of elements in a chunk is unimportant
						result_iterable = pool.imap_unordered(cls._atomic_task_create_independent_global_graph0, distribution, 1)
						for graph in  result_iterable:
							cls.global_graph.update(graph)
			else:
				if reverse:
					for initial in range(max_initial_value, min_initial_value-1, -1):
						if initial not in excludes:
							cls(initial, populate_global_graph = True)
				else:
					for initial in range(min_initial_value, max_initial_value+1):
						if initial not in excludes:
							cls(initial, populate_global_graph = True)
			return cls.global_graph
	
	
	@classmethod
	def _atomic_task_total_stopping_time(cls, start:int) -> int:
		"""
		An elementary task executed by the workers.
		
		Here, the tasks consists of computing the total stopping time for the `Syracuse(start)` sequence.
		"""
		return cls(start).total_stopping_time
	
	@classmethod
	def total_stopping_times_range(cls, max_initial_value:int, min_initial_value:int = 1, parallel:bool = False) -> Tuple[int]:
		"""Generate the tuple of the total stopping times of all Collatz sequences with initial values from `min_initial_value` to `max_initial_value`.
		
		It is possible to switch to an alternative computation algorithm, using the ability of the computer/OS to execute simultaneous tasks. Depending on the hardware (ie: number of "cores" of the CPU), the benefit can be really interesting for a large range of values (the definition of "large" depends heavily on your configuration). For the most little ranges, it is better to use the classical, sequential approach.
			
		Parameters:
			min_initial_value:
				The minimal initial value of the proceeded sequences
			max_initial_value:
				The maximal initial value of the proceeded sequences
			parallel:
				If True, activates the parallel computation algorithm, using pool of multiprocessing workers
		
		Returns:
			The ordered total stopping times of the Collatz sequences
		
		Raises:
			ValueError:
				Raises if `min_initial_value` or `max_initial_value` are not strictly positive integers, or if `max_initial_value` < `min_initial_value`.
		"""

		if not isinstance(max_initial_value, int) or (max_initial_value <= 0):
			raise ValueError("max_initial_value must be a strictly positive integer")
		elif not isinstance(min_initial_value, int) or (min_initial_value <= 0):
			raise ValueError("min_initial_value must be a strictly positive integer")
		elif max_initial_value < min_initial_value:
			raise ValueError("max_initial_value must be greater than min_initial_value")
		else:
			if parallel:
				with Pool() as pool: # Number of worker processes: os.cpu_count() (default)
					# Leave Python computes the chunksize (see https://github.com/python/cpython/blob/3.11/Lib/multiprocessing/pool.py#L481 for details)
					return tuple(pool.map(cls._atomic_task_total_stopping_time, range(min_initial_value, max_initial_value+1)))
			else:
				total_stopping_times_list = []
				for initial in range(min_initial_value, max_initial_value+1):
					total_stopping_times_list.append(cls(initial).total_stopping_time)
				return tuple(total_stopping_times_list)
	
	@classmethod
	def _atomic_task_max(cls, start:int) -> int:
		"""
		An elementary task executed by the workers.
		
		Here, the tasks consists of computing the maximum value for the `Syracuse(start)` sequence.
		"""
		return cls(start).max
	
	@classmethod
	def max_reached_values_range(cls, max_initial_value:int, min_initial_value:int = 1, parallel:bool = False) -> Tuple[int]:
		"""Generate the tuple of the maximal values reached in all Collatz sequences with initial values from `min_initial_value` to `max_initial_value`.
		
		It is possible to switch to an alternative computation algorithm, using the ability of the computer/OS to execute simultaneous tasks. Depending on the hardware (ie: number of "cores" of the CPU), the benefit can be really interesting for a large range of values (the definition of "large" depends heavily on your configuration). For the most little ranges, it is better to use the classical, sequential approach.
			
		Parameters:
			min_initial_value:
				The minimal initial value of the proceeded sequences
			max_initial_value:
				The maximal initial value of the proceeded sequences
			parallel:
				If True, activates the parallel computation algorithm, using pool of multiprocessing workers
		
		Returns:
			A tuple with the ordered maximal reached values of the Collatz sequences
		
		Raises:
			ValueError:
				Raises if `min_initial_value` or `max_initial_value` are not strictly positive integers, or if `max_initial_value` < `min_initial_value`.
		"""
		if not isinstance(max_initial_value, int) or (max_initial_value <= 0):
			raise ValueError("max_initial_value must be a strictly positive integer")
		elif not isinstance(min_initial_value, int) or (min_initial_value <= 0):
			raise ValueError("min_initial_value must be a strictly positive integer")
		elif max_initial_value < min_initial_value:
			raise ValueError("max_initial_value must be greater than min_initial_value")
		else:
			if parallel:
				with Pool() as pool: # Number of worker processes: os.cpu_count() (default)
					# Leave Python computes the chunksize (see https://github.com/python/cpython/blob/3.11/Lib/multiprocessing/pool.py#L481 for details)
					return tuple(pool.map(cls._atomic_task_max, range(min_initial_value, max_initial_value+1)))
			else:
				max_reached_values_list = []
				for initial in range(min_initial_value, max_initial_value+1):
					max_reached_values_list.append(cls(initial).max)
				return tuple(max_reached_values_list)
	
	@classmethod
	def reset_global_graph(cls) -> None:
		"""
		Reset all graphs recorded in the class level: the global graph and the single_graphs list.
		"""
		cls.global_graph = nx.DiGraph()
		cls.single_graphs = {}
		

class CompressedSyracuse(Syracuse):
	"""
	A compressed Collatz sequence instanciated with a given initial value.
	
	This class provides the same parameters, attributes and methods as the inherited Syracuse class.
	"""
	
	def __iter__(self):
		Un = self._initial
		yield Un # Don't forget to yield the initial value !
		while True:
			Un = (Un*3+1)//2 if Un%2 else Un//2
			yield Un