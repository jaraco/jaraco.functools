v4.1.0
======

Features
--------

- Added chainable decorator.


v4.0.2
======

No significant changes.


v4.0.1
======

No significant changes.


v4.0.0
======

Features
--------

- Added ``splat`` function.


Deprecations and Removals
-------------------------

- Removed deprecated 'call_aside'. (#21)


v3.9.0
======

Features
--------

- Enhanced type hints and declare the package as typed. Module is now a package. (#22)


v3.8.1
======

Bugfixes
--------

- Restored type checking and repaired broken exclusion. (#50550895)


v3.8.0
======

Features
--------

- Require Python 3.8 or later.


v3.7.0
======

Added ``bypass_unless`` and ``bypass_when`` and ``identity``.

v3.6.0
======

#21: Renamed ``call_aside`` to ``invoke``, deprecating ``call_aside``.

v3.5.2
======

Refreshed packaging.

v3.5.1
======

Packaging refresh.

Enrolled with Tidelift.

v3.5.0
======

* #19: Add type annotations to ``method_cache``.
* Require Python 3.7.

v3.4.0
======

``apply`` now uses ``functools.wraps`` to ensure docstring
passthrough.

v3.3.0
======

#18: In method_cache, support cache_clear before cache
is initialized.

v3.2.1
======

Refreshed package metadata.

v3.2.0
======

Switched to PEP 420 for ``jaraco`` namespace.

v3.1.0
======

Added ``except_`` decorator.

v3.0.1
======

#14: Removed unnecessary compatibility libraries in testing.

v3.0.0
======

Require Python 3.6 or later.

2.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

1.20
====

Added ``save_method_args``, adopted from ``irc.functools``.

1.19
====

Added ``.reset`` support to ``once``.

1.18
====

Add ``result_invoke`` decorator.

1.17
====

Add ``retry`` decorator.

1.16
====

#7: ``retry_call`` now accepts infinity for the ``retries``
parameter.

1.15.2
======

Refresh packaging.

1.15.1
======

Fix assign_params on Python 2.

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
