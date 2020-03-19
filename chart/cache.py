from datetime import datetime
from typing import Optional, cast

import pandas as pd

from fun.chart.base import CHART_SIZE, LARGE_CHART, MEDIUM_CHART, SMALL_CHART
from fun.chart.static import CandleSticks
from fun.utils import colors, pretty


class QuotesCache:
    def __init__(
        self,
        quotes: pd.DataFrame,
        stime: datetime,
        etime: datetime,
        chart_size: CHART_SIZE = MEDIUM_CHART,
    ):

        assert quotes is not None
        assert chart_size in (SMALL_CHART, MEDIUM_CHART, LARGE_CHART)

        self._quotes = quotes
        self._chart_size = chart_size

        self.time_slice(stime, etime)
        self._make_chart()

    def exstime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._quotes.index[0])

    def exetime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._quotes.index[-1])

    def stime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._stime)

    def etime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._etime)

    def sindex(self) -> int:
        return self._sindex

    def eindex(self) -> int:
        return self._eindex

    def full_quotes(self) -> pd.DataFrame:
        return self._quotes

    def quotes(self) -> pd.DataFrame:
        return self._quotes.loc[self._stime : self._etime]

    def chart(self) -> CandleSticks:
        return self._chart

    def time_slice(self, stime: datetime, etime: datetime) -> None:
        s = self._quotes.loc[stime:etime]

        self._sindex = self._quotes.index.get_loc(s.index[0])
        self._eindex = self._quotes.index.get_loc(s.index[-1])

        self._index_time()

    def _make_chart(self) -> None:
        self._chart = CandleSticks(self.quotes(), chart_size=self._chart_size)

    def _index_time(self) -> None:
        self._stime = self._quotes.index[self._sindex]
        self._etime = self._quotes.index[self._eindex]

    def forward(self) -> Optional[CandleSticks]:
        if self._eindex == len(self._quotes) - 1:
            pretty.color_print(colors.PAPER_AMBER_300, "cache is at the last quote")
            return None

        self._sindex += 1
        self._eindex += 1

        self._index_time()
        self._make_chart()

        return self.chart()

    def backward(self) -> Optional[CandleSticks]:
        if self._sindex == 0:
            pretty.color_print(colors.PAPER_AMBER_300, "cache is at the first quote")
            return None

        self._sindex -= 1
        self._eindex -= 1

        self._index_time()
        self._make_chart()

        return self.chart()
