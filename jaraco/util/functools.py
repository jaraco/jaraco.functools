def compose(*funcs):
	"""
	Compose any number of unary functions into a single unary
	function.
	
	>>> import textwrap
	>>> str.strip(textwrap.dedent(compose.__doc__)) == compose(str.strip, textwrap.dedent)(compose.__doc__)
	True
	"""
	
	compose_two = lambda f1, f2: lambda v: f1(f2(v))
	return reduce(compose_two, funcs)
