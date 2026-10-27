import inspect

import pytest

from jaraco.functools import once


@pytest.mark.parametrize('saved_result', [None, 0, 99])
def test_once_does_not_inherit_saved_result(saved_result: object) -> None:
    calls = []

    def func(value: int) -> int:
        calls.append(value)
        return value + 1

    vars(func)['saved_result'] = saved_result
    vars(func)['custom'] = 'metadata'
    wrapped = once(func)

    assert wrapped(2) == 3
    assert wrapped(8) == 3
    assert calls == [2]
    assert vars(func)['saved_result'] is saved_result
    assert vars(wrapped)['custom'] == 'metadata'
    assert inspect.unwrap(wrapped) is func

    wrapped.reset()
    assert wrapped(8) == 9
    delattr(wrapped, 'saved_result')
    assert wrapped(4) == 5
    assert calls == [2, 8, 4]


def test_once_nested_wrapper_observes_reset_before_first_call() -> None:
    calls = []

    def func(value: int) -> int:
        calls.append(value)
        return value + 1

    inner = once(func)
    assert inner(2) == 3
    outer = once(inner)
    inner.reset()

    assert outer(8) == 9
    assert outer(10) == 9
    assert calls == [2, 8]
