1.15.1
======

Refresh packaging.

1.15
====

Add ``assign_params`` function.

1.14
====

Add ``pass_none`` decorator function.

1.13
====

Add ``print_yielded`` func implementing the func of the same
name found in autocommand docs.

1.12
====

Issue #6: Added a bit of documentation and xfail tests showing
that the ``method_cache`` can't be used with other decorators
such as ``property``.

1.11
====

Include dates and links in changelog.

1.10
====

Use Github for continuous deployment to PyPI.

1.9
===

Add ``retry_call``, a general-purpose function retry mechanism.
See ``test_functools`` for tests and example usage.

1.8
===

More generous handling of missing lru_cache when installed on
Python 2 and older pip. Now all functools except ``method_cache``
will continue to work even if ``backports.functools_lru_cache``
is not installed. Also allows functools32 as a fallback if
available.

1.7
===

Moved hosting to github.

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
