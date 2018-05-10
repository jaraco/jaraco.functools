import itertools
import time
import copy
import random
import functools
from unittest import mock

import pytest
from jaraco.classes import properties

from jaraco.functools import Throttler, method_cache, retry_call, retry

__metaclass__ = type


class TestThrottler:
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
		class ThrottledMethodClass:
			@Throttler
			def echo(self, arg):
				return arg

		tmc = ThrottledMethodClass()
		assert tmc.echo('foo') == 'foo'


class TestMethodCache:
	bad_vers = '(3, 5, 0) <= sys.version_info < (3, 5, 2)'

	@pytest.mark.skipif(bad_vers, reason="https://bugs.python.org/issue25447")
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

	def test_special_methods(self):
		"""
		Test method_cache with __getitem__ and __getattr__.
		"""
		class ClassUnderTest:
			getitem_calls = 0
			getattr_calls = 0

			@method_cache
			def __getitem__(self, item):
				self.getitem_calls += 1
				return item

			@method_cache
			def __getattr__(self, name):
				self.getattr_calls += 1
				return name

		ob = ClassUnderTest()

		# __getitem__
		ob[1] + ob[1]
		assert ob.getitem_calls == 1

		# __getattr__
		ob.one + ob.one
		assert ob.getattr_calls == 1

	@pytest.mark.xfail(reason="can't replace property with cache; #6")
	def test_property(self):
		"""
		Can a method_cache decorated method also be a property?
		"""
		class ClassUnderTest:
			@property
			@method_cache
			def mything(self):
				return random.random()

		ob = ClassUnderTest()

		assert ob.mything == ob.mything

	@pytest.mark.xfail(reason="can't replace property with cache; #6")
	def test_non_data_property(self):
		"""
		A non-data property also does not work because the property
		gets replaced with a method.
		"""
		class ClassUnderTest:
			@properties.NonDataProperty
			@method_cache
			def mything(self):
				return random.random()

		ob = ClassUnderTest()

		assert ob.mything == ob.mything


class TestRetry:
	def attempt(self, arg=None):
		if next(self.fails_left):
			raise ValueError("Failed!")
		if arg:
			arg.touch()
		return "Success"

	def set_to_fail(self, times):
		self.fails_left = itertools.count(times, -1)

	def test_set_to_fail(self):
		"""
		Test this test's internal failure mechanism.
		"""
		self.set_to_fail(times=2)
		with pytest.raises(ValueError):
			self.attempt()
		with pytest.raises(ValueError):
			self.attempt()
		assert self.attempt() == 'Success'

	def test_retry_call_succeeds(self):
		self.set_to_fail(times=2)
		res = retry_call(self.attempt, retries=2, trap=ValueError)
		assert res == "Success"

	def test_retry_call_fails(self):
		"""
		Failing more than the number of retries should
		raise the underlying error.
		"""
		self.set_to_fail(times=3)
		with pytest.raises(ValueError) as res:
			retry_call(self.attempt, retries=2, trap=ValueError)
		assert str(res.value) == 'Failed!'

	def test_retry_multiple_exceptions(self):
		self.set_to_fail(times=2)
		errors = ValueError, NameError
		res = retry_call(self.attempt, retries=2, trap=errors)
		assert res == "Success"

	def test_retry_exception_superclass(self):
		self.set_to_fail(times=2)
		res = retry_call(self.attempt, retries=2, trap=Exception)
		assert res == "Success"

	def test_default_traps_nothing(self):
		self.set_to_fail(times=1)
		with pytest.raises(ValueError):
			retry_call(self.attempt, retries=1)

	def test_default_does_not_retry(self):
		self.set_to_fail(times=1)
		with pytest.raises(ValueError):
			retry_call(self.attempt, trap=Exception)

	def test_cleanup_called_on_exception(self):
		calls = random.randint(1, 10)
		cleanup = mock.Mock()
		self.set_to_fail(times=calls)
		retry_call(self.attempt, retries=calls, cleanup=cleanup, trap=Exception)
		assert cleanup.call_count == calls
		assert cleanup.called_with()

	def test_infinite_retries(self):
		self.set_to_fail(times=999)
		cleanup = mock.Mock()
		retry_call(
			self.attempt, retries=float('inf'), cleanup=cleanup,
			trap=Exception)
		assert cleanup.call_count == 999

	def test_with_arg(self):
		self.set_to_fail(times=0)
		arg = mock.Mock()
		bound = functools.partial(self.attempt, arg)
		res = retry_call(bound)
		assert res == 'Success'
		assert arg.touch.called

	def test_decorator(self):
		self.set_to_fail(times=1)
		attempt = retry(retries=1, trap=Exception)(self.attempt)
		res = attempt()
		assert res == "Success"

	def test_decorator_with_arg(self):
		self.set_to_fail(times=0)
		attempt = retry()(self.attempt)
		arg = mock.Mock()
		res = attempt(arg)
		assert res == 'Success'
		assert arg.touch.called
