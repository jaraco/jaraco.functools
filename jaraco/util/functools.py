from __future__ import absolute_import, unicode_literals

import functools

def compose(*funcs):
	"""
	Compose any number of unary functions into a single unary function.

	>>> import textwrap
	>>> from six import text_type
	>>> text_type.strip(textwrap.dedent(compose.__doc__)) == compose(text_type.strip, textwrap.dedent)(compose.__doc__)
	True

	Compose also allows the innermost function to take arbitrary arguments.

	>>> round_three = lambda x: round(x, ndigits=3)
	>>> f = compose(round_three, int.__truediv__)
	>>> [f(3*x, x+1) for x in range(1,10)]
	[1.5, 2.0, 2.25, 2.4, 2.5, 2.571, 2.625, 2.667, 2.7]
	"""

	compose_two = lambda f1, f2: lambda *args, **kwargs: f1(f2(*args, **kwargs))
	return functools.reduce(compose_two, funcs)

def method_caller(method_name, *args, **kwargs):
	"""
	Return a function that will call a named method on the
	target object with optional positional and keyword
	arguments.

	>>> lower = method_caller('lower')
	>>> lower('MyString')
	'mystring'
	"""
	def call_method(target):
		func = getattr(target, method_name)
		return func(*args, **kwargs)
	return call_method

def once(func):
	"""
	Decorate func so it's only ever called the first time.

	This decorator can ensure that an expensive or non-idempotent function
	will not be expensive on subsequent calls and is idempotent.

	>>> func = once(lambda a: a+3)
	>>> func(3)
	6
	>>> func(9)
	6
	>>> func('12')
	6
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if not hasattr(func, 'always_returns'):
			func.always_returns = func(*args, **kwargs)
		return func.always_returns
	return wrapper

def method_cache(method):
	"""
	Wrap lru_cache to support storing the cache data in the object instances.

	Abstracts the common paradigm where the method explicitly saves an
	underscore-prefixed protected property on first call and returns that
	subsequently.

	>>> class MyClass:
	...     calls = 0
	...
	...     @method_cache
	...     def method(self, value):
	...         self.calls += 1
	...         return value

	>>> a = MyClass()
	>>> a.method(3)
	3
	>>> for x in range(75):
	...     res = a.method(x)
	>>> a.calls
	75

	Note that the apparent behavior will be exactly like that of lru_cache
	except that the cache is stored on each instance, so values in one
	instance will not flush values from another, and when an instance is
	deleted, so are the cached values for that instance.

	>>> b = MyClass()
	>>> for x in range(35):
	...     res = b.method(x)
	>>> b.calls
	35
	>>> a.method(0)
	0
	>>> a.calls
	75

	Note that if method had been decorated with ``functools.lru_cache()``,
	a.calls would have been 76 (due to the cached value of 0 having been
	flushed by the 'b' instance).
	"""
	# todo: allow the cache to be customized
	cache_wrapper = functools.lru_cache()
	def wrapper(self, *args, **kwargs):
		# it's the first call, replace the method with a cached, bound method
		bound_method = functools.partial(method, self)
		cached_method = cache_wrapper(bound_method)
		setattr(self, method.__name__, cached_method)
		return cached_method(*args, **kwargs)
	return wrapper
