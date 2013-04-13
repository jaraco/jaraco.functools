from __future__ import absolute_import, unicode_literals

import functools

def compose(*funcs):
	"""
	Compose any number of unary functions into a single unary function.

	>>> import textwrap
	>>> unicode.strip(textwrap.dedent(compose.__doc__)) == compose(unicode.strip, textwrap.dedent)(compose.__doc__)
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
	u'mystring'
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
