import subprocess
import sys
import textwrap

import pytest


@pytest.mark.parametrize('optimization', ['', '-O', '-OO'])
def test_chainable_invokes_method(optimization: str) -> None:
    code = textwrap.dedent('''
        from jaraco.functools import chainable

        class Counter:
            def __init__(self):
                self.value = 0

            @chainable
            def add(self, amount, *, multiplier=1):
                self.value += amount * multiplier

        counter = Counter()
        result = counter.add(3, multiplier=2).add(4)
        print(counter.value, result is counter)
    ''')
    command = [sys.executable, *filter(None, [optimization]), '-c', code]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    assert result.stdout == '10 True\n'
