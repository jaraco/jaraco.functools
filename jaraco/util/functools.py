from __future__ import absolute_import, unicode_literals

import functools

def compose(*funcs):
	"""
	Compose any number of unary functions into a single unary
	function.

	>>> import textwrap
	>>> unicode.strip(textwrap.dedent(compose.__doc__)) == compose(unicode.strip, textwrap.dedent)(compose.__doc__)
	True
	"""

	compose_two = lambda f1, f2: lambda v: f1(f2(v))
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
