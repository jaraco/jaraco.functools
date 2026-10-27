from __future__ import annotations

from jaraco.functools import Throttler


class Example:
    @Throttler
    def method(self, value: int) -> tuple[Example, int]:
        return self, value


def test_class_access_preserves_descriptor() -> None:
    assert Example.method is vars(Example)['method']


def test_unbound_method_call() -> None:
    instance = Example()
    assert Example.method(instance, value=42) == (instance, 42)


def test_bound_method_call() -> None:
    instance = Example()
    assert instance.method(value=42) == (instance, 42)
