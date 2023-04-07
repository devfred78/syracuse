"""
This module provides several well-known sequences related to Collatz sequences.

Unless explicitely mentioned, all sequences provided here implement the [iterator protocol](https://docs.python.org/3/library/stdtypes.html#iterator-types). That is, they can be used in `for` loops, and as parameter for the built-in `iter()` and `next()` functions. It also means that only one item is kept in memory at a time, the next items being generated on demand or lazily. Unlike container types like lists or dictionnaries, data are not stored but forgotten once the next item is yield. By the way, iterators are very memory-efficient and can process infinite data streams, like most of the sequences generated here.

The available sequences are the following:

| sequence | [OEIS](https://oeis.org/) reference | Description |
| -------- | ----------------------------------- | ----------- |
| total_stopping_time_records | A006877 | Sequence of starting values of Collatz sequences with a total stopping time longer than of any smaller starting value. |


"""

from collections import namedtuple
from collections.abc import Iterator
from itertools import count

from gmpy2 import bit_scan1

Record = namedtuple("Record", "rank value")

class total_stopping_time_records(Iterator):
	"""
	Sequence of starting values of Collatz sequences with a total stopping time longer than of any smaller starting value. OEIS reference: [A006877](https://oeis.org/A006877).
	
	!!! example
		
		6 is included in this sequence because the total stopping time of the Collatz sequence beginning by 6 (that is, 8) is greater than total stopping times of all Collatz sequences beginning by 1, 2, 3, 4 and 5.
	
	In order to speedup the computation, it is possible to apply optional optimizations. Those optimizations are combinable (by addition of their number) for a greater efficiency. Deeper details (including mathematical demontrations) are available in [this article from T. Leavens and M. Vermeulen](https://oeis.org/A006877/a006877_1.pdf).
	
	The available sorts of optimizations are the following (the speedup factor is calculated with the first 50 records. It is only indicative, since it may differ on your own configuration):
	
	| Number | Name | Description | Speedup factor |
	| ------ | ---- | ----------- | -------------- |
	| 0      | None | No optimization | 1.0 |
	| 1      | Even numbers | Due to the fact that `Syracuse(2k).total_stopping_time` = `Syracuse(k).total_stopping_time + 1`, it is easy to predict the next even candidate for this sequence, and then it is not necessary to compute the Collatz sequences for the other event numbers below this candidate. | 1.8 |
	| 2      | k mod 6 = 5 | If the remainder of the division of the initial value by 6 is 5, then this cannot be a record for the total stopping time. | 1.2 |
	| 4      | *a posteriori* cutoff | It is possible to stop the iteration process of a Collatz sequence before its end, by comparing the current iterate value with all previous records and the number of steps necessary to reach it. **This optimization needs to store all items previously computed, making this iterator less memory-efficient**. | 2.0 |
	| 8      | make_odd | Speed up the iterations of the Collatz sequences by replacing the successive divisions by 2, by only one step. Be aware that using this "optimization" alone is absolutly not efficient (as you can see, the speedup factor is less than 1, meaning that it is better not to use it !). However, it is a really "booster" when associated with other optimization algorithms. For instance, the *a posteriori* cutoff is boosted with a speedup factor of 3.7 when used together with the "make_odd" one. | 0.76 |
	
	Parameters:
		optimization:
			Type of optimization(s) applied. No optimization by default.
	"""
	
	# Optimizations
	NO_OPT = 0
	EVEN_OPT = 1
	KMOD6_OPT = 2
	APOST_OPT = 4
	MKODD_OPT = 8
	
	def __init__(self, optimization:int = 0):
		self.optimization = optimization
		self.previous_record = -1
		if self.optimization & self.EVEN_OPT:
			self.previous_rank = 0
		if self.optimization & self.APOST_OPT:
			self.records = list()
	
	def __next__(self):
		n = 1
		while True:
			optim_applied = False
			if (self.optimization & self.KMOD6_OPT) and (n%6 == 5):
				# No value must be returned this time
				value = self.previous_record
				optim_applied = True

			if (self.optimization & self.EVEN_OPT) and not n%2:
				if n == self.previous_rank * 2:
					value = self._steps_mkodd(n) if (self.optimization & self.MKODD_OPT) else self._steps_apost(n) if (self.optimization & self.APOST_OPT) else self._steps(n)
					optim_applied = True
				else:
					# No value must be returned this time
					value = self.previous_record
					optim_applied = True
			
			if not optim_applied:
				value = self._steps_mkodd(n) if (self.optimization & self.MKODD_OPT) else self._steps_apost(n) if (self.optimization & self.APOST_OPT) else self._steps(n)
			
			if value is not None and (value > self.previous_record):
				self.previous_record = value
				if self.optimization & self.EVEN_OPT:
					self.previous_rank = n
				if self.optimization & self.APOST_OPT:
					self.records.append(Record(rank=n, value=value))
				return n
			n += 1
	
	def _steps(self, n:int) -> int:
		"""
		The total stopping time of the Collatz sequence beginning by `n`.
		
		Since the values of the Collatz sequence are not stored, the usage of a syracuse.Syracuse() instance is not necessary.
		
		Parameters:
			n:
				Initial value of the Collatz sequence for which the total stopping time is calculated.
		
		Returns:
			The total stopping time.
		
		Raises:
			ValueError:
				Raises if `n` is not a strictly positive integer.
		"""
		
		if n<=0 or not isinstance(n, int):
			raise ValueError(f"{n} is not a strictly positive integer")

		steps = 0
		
		while n>1:
			n = n*3+1 if n%2 else n//2
			steps += 1
		
		return steps
	
	def _steps_apost(self, n:int) -> int|None:
		"""
		The total stopping time of the Collatz sequence beginning by `n`, using the *a posteriori* cutoff optimization.
		
		If the *a posteriori* cutoff algorithm concludes that the current Collatz sequence is not a record, then it is immediatly dropped of, and the function returns `None`.
		
		Parameters:
			n:
				Initial value of the Collatz sequence for which the total stopping time is calculated.
		
		Returns:
			The total stopping time, or `None` if the iteration process has been stopped before its end.
		
		Raises:
			ValueError:
				Raises if `n` is not a strictly positive integer.
		"""
		
		if n<=0 or not isinstance(n, int):
			raise ValueError(f"{n} is not a strictly positive integer")

		steps = 0
		
		while n>1:
			if n%2:
				n = n*3+1
				steps += 1
			else:
				n = n//2
				steps += 1
				if len(self.records) > 0:
					upper_records = [record for record in self.records if n < record.rank]
					for record in upper_records:
						if steps + record.value <= self.previous_record:
							return
					
		return steps
	
	def _make_odd(self, n:int) -> tuple[int, int|None]:
		"""
		Divides by 2 the given strictly positive integer multiple times until it becomes odd.
		
		The division sequence is made by bit shifting, using a heavily optimized function provided by the [gmpy2 module](https://gmpy2.readthedocs.io/en/latest/mpz.html#gmpy2.bit_scan1).
		Returns the odd value reached and the number of divisions needed.
		
		Parameters:
			n:
				Value to make odd
		
		Returns:
			n: resulting odd value reached
			steps: number of divisions needed to reach the odd value
		
		Raises:
			ValueError:
				Raises if `n` is not a strictly positive integer.
		"""
		if n<=0 or not isinstance(n, int):
			raise ValueError(f"{n} is not a strictly positive integer")
		
		steps = 0
		
		if (steps := bit_scan1(n)):
			n>>=steps

		return n, steps
	
	def _steps_mkodd(self, n:int) -> int|None:
		"""
		The total stopping time of the Collatz sequence beginning by `n`, using the "make_odd" optimization.
		
		This method implements also the optional, *a posteriori* cutoff optimization.
		
		Parameters:
			n:
				Initial value of the Collatz sequence for which the total stopping time is calculated.
		
		Returns:
			The total stopping time, or `None` if the iteration process has been stopped before its end (if the *a posteriori* cutoff optimization is activated).
		
		Raises:
			ValueError:
				Raises if `n` is not a strictly positive integer.
		"""
		
		if n<=0 or not isinstance(n, int):
			raise ValueError(f"{n} is not a strictly positive integer")

		steps = 0
		
		while n>1:
			if n%2:
				n = n*3+1
				steps += 1
			
			# At this step, n is necessarily even
			n, p = self._make_odd(n)
			steps += p
			
			# Optional, *a posteriori* cutoff optimization
			if (self.optimization & self.APOST_OPT):
				if len(self.records) > 0:
					upper_records = [record for record in self.records if n < record.rank]
					for record in upper_records:
						if steps + record.value <= self.previous_record:
							return

		return steps