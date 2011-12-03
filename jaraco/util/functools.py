from __future__ import absolute_import, unicode_literals
from functools import reduce

def compose(*funcs):
	"""
	Compose any number of unary functions into a single unary
	function.

	>>> import textwrap
	>>> unicode.strip(textwrap.dedent(compose.__doc__)) == compose(unicode.strip, textwrap.dedent)(compose.__doc__)
	True
	"""

	compose_two = lambda f1, f2: lambda v: f1(f2(v))
	return reduce(compose_two, funcs)

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
