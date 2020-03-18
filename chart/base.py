import io
import re
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, List, NewType, Optional, Tuple, Union, cast

import numpy as np
import pandas as pd

from fun.chart.indicator import bollinger_band, simple_moving_average
from fun.trading.transaction import FuturesTransaction

CHART_SIZE = NewType("CHART_SIZE", int)
LARGE_CHART = CHART_SIZE(0)
MEDIUM_CHART = CHART_SIZE(1)
SMALL_CHART = CHART_SIZE(2)


class BaseChart(metaclass=ABCMeta):
    def __init__(
        self, quotes: pd.DataFrame, chart_size: CHART_SIZE = LARGE_CHART
    ) -> None:

        assert quotes is not None
        assert chart_size in (LARGE_CHART, MEDIUM_CHART, SMALL_CHART)

        self._quotes = quotes
        self._chart_size = chart_size

        self._simple_moving_averages()
        self._bollinger_bands()

    def _minimum_body_height(self) -> float:
        mn, mx = self._ylim_from_price_range()
        r = mx - mn

        return r * 0.0025

    def _ylim_from_price_range(self) -> Tuple[float, float]:
        extend_ratio = 25.0

        mn = np.amin(self._quotes.loc[:, "low"])
        mx = np.amax(self._quotes.loc[:, "high"])

        r = mx - mn

        return (
            mn - (r / extend_ratio),
            mx + (r / extend_ratio),
        )

    def _simple_moving_averages(self) -> None:
        self._quotes = simple_moving_average(self._quotes, 5)
        self._quotes = simple_moving_average(self._quotes, 20)

    def _simple_moving_averages_extend(self) -> None:
        self._quotes = simple_moving_average(self._quotes, 50)
        self._quotes = simple_moving_average(self._quotes, 200)

    def _bollinger_bands(self) -> None:
        self._quotes = bollinger_band(self._quotes, 20, 1.5)
        self._quotes = bollinger_band(self._quotes, 20, 2.0)
        self._quotes = bollinger_band(self._quotes, 20, 2.5)
        self._quotes = bollinger_band(self._quotes, 20, 3.0)

    def _plot_trading_records(
        self,
        records: List[FuturesTransaction],
        cb: Callable[[int, float, str, str, str], Any],
    ) -> None:

        pass

        # table = {
        # "long": "L",
        # "short": "S",
        # "increase": "A",
        # "decrease": "D",
        # "close": "X",
        # }

        # mn, mx = self._ylim_from_price_range()
        # m = (mn + mx) / 2.0

        # records.sort(key=lambda x: x.time_stamp)

        # ts: Dict[int, Dict[str, Any]] = {}

        # for i, t in enumerate(self._quotes.index):

        # s = t
        # e: datetime
        # if i + 1 < len(self._quotes.index):
        # e = self._quotes.index[i + 1]
        # else:
        # e = s + timedelta(days=365)

        # assert e is not None

        # for i, r in enumerate(records):
        # rt = r.time

        # x: Optional[int] = None
        # op: Optional[str] = None
        # if rt >= s and rt < e:
        # x = self._quotes.index.get_loc(s)
        # op = r.operation

        # if x is None or op is None:
        # continue

        # assert x is not None
        # assert op is not None

        # assert op in tuple(table.keys())

        # t = table[op]

        # h = self._quotes.iloc[x]["high"]
        # l = self._quotes.iloc[x]["low"]
        # pm = (h + l) / 2.0

        # y = 0
        # va = ""

        # if pm > m:
        # y = l - self._body_min_height * 2
        # va = "top"
        # else:
        # y = h + self._body_min_height * 2
        # va = "bottom"

        # if x in ts:
        # ts[x]["t"].append(t)
        # else:
        # ts[x] = {}
        # ts[x]["y"] = y
        # ts[x]["va"] = va
        # ts[x]["t"] = [t]

        # for x, vs in ts.items():

        # y = vs["y"]
        # t = "\n".join(vs["t"])

        # ha = "center"
        # va = vs["va"]

        # cb(x, y, t, ha, va)

    def _plot_indicators(self, cb: Callable[[str, str, str], Any]) -> None:
        smas = [col for col in self._quotes.columns if "sma" in col]
        bbs = [col for col in self._quotes.columns if "bb" in col]

        if len(smas) > 0:
            smas.sort(key=lambda x: int(x.replace("sma", "")))

            for i, col in enumerate(smas):
                cb(col, f"sma{i}", "sma")

        if len(bbs) > 0:
            bbs.sort(
                key=lambda x: (
                    float(cast(re.Match, re.match(r"bb\d+[+-]([0-9.]+)", x)).group(1))
                )
            )

            last = 0.0
            ci = -1
            for col in bbs:

                m = re.match(r"bb\d+[+-]([0-9.]+)", col)
                assert m is not None
                c = abs(float(m.group(1)))
                if c != last:
                    ci += 1
                    last = c

                cb(col, f"bb{ci}", "bb")

    @abstractmethod
    def futures_price(
        self,
        output: Union[str, io.BytesIO],
        records: Optional[List[FuturesTransaction]] = None,
        interactive: bool = False,
    ) -> None:
        raise NotImplementedError
