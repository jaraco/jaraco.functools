1.6
===

``method_cache`` now accepts a cache_wrapper parameter, allowing
for custom parameters to an ``lru_cache`` or an entirely different
cache implementation.

Use ``backports.functools_lru_cache`` to provide ``lru_cache`` for
Python 2.

1.5
===

Implement ``Throttler`` as a descriptor so it may be used to decorate
methods. Introduces ``first_invoke`` function.

Fixed failure in Throttler on Python 2 due to improper use of integer
division.

1.4
===

Added ``Throttler`` class from `irc <https://bitbucket.org/jaraco/irc>`_.

1.3
===

Added ``call_aside`` decorator.

1.2
===

Added ``apply`` decorator.

1.0
===

Initial release drawn from jaraco.util.
