import functools
from typing import Dict, Any, List
from fun.utils import pretty, colors


def parameterized(sets: List[Dict[str, Any]]):
    def testing(func):
        @functools.wraps(func)
        def wrapper_testing(*args, **kargs):
            pretty.color_print(
                colors.PAPER_LIGHT_BLUE_300,
                f"running {len(sets)} parameterized tests",
            )
            for book in sets:
                func(*args, **book)

        return wrapper_testing

    return testing
