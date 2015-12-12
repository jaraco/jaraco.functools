import itertools
import time
import copy
import sys

import pytest

from jaraco.functools import Throttler, method_cache


class TestThrottler(object):
	def test_function_throttled(self):
		"""
		Ensure the throttler actually throttles calls.
		"""
		# set up a function to be called
		counter = itertools.count()
		# set up a version of `next` that is only called 30 times per second
		limited_next = Throttler(next, 30)
		# for one second, call next as fast as possible
		deadline = time.time() + 1
		while time.time() < deadline:
			limited_next(counter)
		# ensure the counter was advanced about 30 times
		assert 28 <= next(counter) <= 32

		# ensure that another burst of calls after some idle period will also
		# get throttled
		time.sleep(1)
		deadline = time.time() + 1
		counter = itertools.count()
		while time.time() < deadline:
			limited_next(counter)
		assert 28 <= next(counter) <= 32

	def test_reconstruct_unwraps(self):
		"""
		The throttler should be re-usable - if one wants to throttle a
		function that's aready throttled, the original function should be
		used.
		"""
		wrapped = Throttler(next, 30)
		wrapped_again = Throttler(wrapped, 60)
		assert wrapped_again.func is next
		assert wrapped_again.max_rate == 60

	def test_throttled_method(self):
		class ThrottledMethodClass(object):
			@Throttler
			def echo(self, arg):
				return arg

		tmc = ThrottledMethodClass()
		assert tmc.echo('foo') == 'foo'


class TestMethodCache:
	@pytest.mark.skipif('sys.version_info == (3, 5, 0)',
		reason="https://bugs.python.org/issue25447")
	def test_deepcopy(self):
		"""
		A deepcopy of an object with a method cache should still
		succeed.
		"""
		class ClassUnderTest:
			calls = 0

			@method_cache
			def method(self, value):
				self.calls += 1
				return value

		ob = ClassUnderTest()
		copy.deepcopy(ob)
		ob.method(1)
		copy.deepcopy(ob)
