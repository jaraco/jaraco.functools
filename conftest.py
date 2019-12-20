import sys
import re

import jaraco.functools


def pytest_configure():
    patch_for_issue_12()


def patch_for_issue_12():  # pragma: nocover
    """
    Issue #12 revealed that Python 3.7.3 had a subtle
    change in the C implementation of functools that
    broke the assumptions around the method_cache (or
    any caller using possibly empty keyword arguments).
    This patch adjusts the docstring for that test so it
    can pass on that Python version.
    """
    affected_ver = 3, 7, 3
    if sys.version_info[:3] != affected_ver:
        return
    mc = jaraco.functools.method_cache
    mc.__doc__ = re.sub(r'^(\s+)75', r'\g<1>76', mc.__doc__, flags=re.M)
