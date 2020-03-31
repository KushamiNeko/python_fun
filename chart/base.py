import io
from abc import ABCMeta, abstractmethod
from typing import List, NewType, Optional, Tuple, Union

import numpy as np
import pandas as pd

# from fun.chart.indicator import bollinger_band, simple_moving_average
# from fun.trading.transaction import FuturesTransaction
from fun.plotter.plotter import Plotter

CHART_SIZE = NewType("CHART_SIZE", int)
LARGE_CHART = CHART_SIZE(0)
MEDIUM_CHART = CHART_SIZE(1)
SMALL_CHART = CHART_SIZE(2)


class ChartFactory(metaclass=ABCMeta):
    def __init__(
        self,
        quotes: pd.DataFrame,
        # extended_quotes: Optional[pd.DataFrame] = None,
        # chart_size: CHART_SIZE = LARGE_CHART,
    ) -> None:

        assert quotes is not None
        # assert chart_size in (LARGE_CHART, MEDIUM_CHART, SMALL_CHART)

        self._quotes = quotes
        # if extended_quotes is None:
        # self._extended_quotes = self._quotes
        # else:
        # self._extended_quotes = extended_quotes

        # self._chart_size = chart_size

    # def _ylim_from_price_range(self) -> Tuple[float, float]:
    # extend_ratio = 25.0

    # mn = np.amin(self._quotes.loc[:, "low"])
    # mx = np.amax(self._quotes.loc[:, "high"])

    # r = mx - mn

    # return (
    # mn - (r / extend_ratio),
    # mx + (r / extend_ratio),
    # )

    def quotes_range(self) -> Tuple[float, float]:
        mn = np.amin(self._quotes.loc[:, "low"])
        mx = np.amax(self._quotes.loc[:, "high"])

        return mn, mx

    def chart_xrange(self) -> Tuple[float, float]:
        return -0.5, (len(self._quotes) - 1) + 0.5

    def chart_yrange(self) -> Tuple[float, float]:
        extend_ratio = 25.0

        mn, mx = self.quotes_range()
        r = mx - mn

        return (
            mn - (r / extend_ratio),
            mx + (r / extend_ratio),
        )

    # def _plot_trading_records(
    # self,
    # records: List[FuturesTransaction],
    # cb: Callable[[int, float, str, str, str], Any],
    # ) -> None:

    # pass

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

    @abstractmethod
    def to_data_coordinates(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        raise NotImplementedError

    @abstractmethod
    def render(
        self,
        output: Union[str, io.BytesIO],
        # records: Optional[List[FuturesTransaction]] = None,
        # show_quote: bool = True,
        interactive: bool = False,
        plotters: Optional[List[Plotter]] = None,
    ) -> None:
        raise NotImplementedError


class CandleSticks(ChartFactory):
    # def __init__(
    # self,
    # quotes: pd.DataFrame,
    # extended_quotes: Optional[pd.DataFrame] = None,
    # chart_size: CHART_SIZE = LARGE_CHART,
    # ) -> None:
    # super().__init__(quotes, extended_quotes, chart_size)

    def _minimum_body_height(self) -> float:
        ratio = 0.0025
        mn, mx = self.quotes_range()
        r = mx - mn

        return r * ratio

    # def _plot_indicators(
    # self, callback: Callable[[pd.DataFrame, str, str], Any]
    # ) -> None:

    # s = self._quotes.index[0]
    # e = self._quotes.index[-1]

    # callback(
    # simple_moving_average(self._extended_quotes.loc[:, "close"], 5).loc[s:e],
    # "sma0",
    # "sma",
    # )

    # callback(
    # simple_moving_average(self._extended_quotes.loc[:, "close"], 20).loc[s:e],
    # "sma1",
    # "sma",
    # )

    # bbs = (1.5, 2.0, 2.5, 3.0)
    # for i, m in enumerate(bbs):
    # up, down = bollinger_band(self._extended_quotes.loc[:, "close"], 20, m)

    # callback(up.loc[s:e], f"bb{i}", "bb")
    # callback(down.loc[s:e], f"bb{i}", "bb")
