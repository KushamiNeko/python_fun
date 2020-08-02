import functools
from typing import Any, Dict, List

from fun.utils import colors, pretty


def parameterized(sets: List[Dict[str, Any]]):
    def testing(func):
        @functools.wraps(func)
        def wrapper_testing(*args, **kargs):
            count = 0
            for book in sets:
                func(*args, **book)
                count += 1

            pretty.color_print(
                    colors.PAPER_LIGHT_BLUE_300, f"\nrunning {count} parameterized tests",
            )

        return wrapper_testing

    return testing
