import time

import pytest

from jaraco.functools import Throttler


@pytest.mark.parametrize('new_wall_time', [10, 2000])
@pytest.mark.parametrize('epoch', [-100, 100])
def test_wall_clock_changes_do_not_change_rate(
    monkeypatch: pytest.MonkeyPatch, new_wall_time: int, epoch: int
) -> None:
    wall_times = iter([1000, 1000, new_wall_time, new_wall_time])
    elapsed_times = iter([epoch, epoch, epoch + 0.25, epoch + 1])
    waits: list[float] = []
    monkeypatch.setattr(time, 'time', lambda: next(wall_times))
    monkeypatch.setattr(time, 'monotonic', lambda: next(elapsed_times))
    monkeypatch.setattr(time, 'sleep', waits.append)
    throttled = Throttler(str, max_rate=1)
    assert throttled(1) == '1'
    assert throttled(2) == '2'
    assert waits == [0, 0.75]
