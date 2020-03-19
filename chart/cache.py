from datetime import datetime
from typing import Optional, cast

import pandas as pd

from fun.chart.base import CHART_SIZE, LARGE_CHART, MEDIUM_CHART, SMALL_CHART
from fun.chart.indicator import bollinger_band, simple_moving_average
from fun.chart.static import CandleSticks


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

        # self._simple_moving_averages()
        # self._bollinger_bands()

        self.time_slice(stime, etime)
        self._make_chart()

    #def _simple_moving_averages(self) -> None:
    #    self._quotes = simple_moving_average(self._quotes, 5)
    #    self._quotes = simple_moving_average(self._quotes, 20)

    #def _simple_moving_averages_extend(self) -> None:
    #    self._quotes = simple_moving_average(self._quotes, 50)
    #    self._quotes = simple_moving_average(self._quotes, 200)

    #def _bollinger_bands(self) -> None:
    #    self._quotes = bollinger_band(self._quotes, 20, 1.5)
    #    self._quotes = bollinger_band(self._quotes, 20, 2.0)
    #    self._quotes = bollinger_band(self._quotes, 20, 2.5)
    #    self._quotes = bollinger_band(self._quotes, 20, 3.0)

    def exstime(self) -> datetime:
        return cast(datetime, self._quotes.index[0].to_pydatetime())
        # return cast(datetime, self._quotes.index[0])

    def exetime(self) -> datetime:
        return cast(datetime, self._quotes.index[-1].to_pydatetime())
        # return cast(datetime, self._quotes.index[-1])

    def stime(self) -> datetime:
        return cast(datetime, self._stime)

    def etime(self) -> datetime:
        return cast(datetime, self._etime)

    def slice(self) -> pd.DataFrame:
        return self._quotes.loc[self._stime : self._etime]

    def chart(self) -> CandleSticks:
        return self._chart

    def time_slice(self, stime: datetime, etime: datetime) -> None:
        s = self._quotes.loc[stime:etime]

        self._sindex = self._quotes.index.get_loc(s.index[0])
        self._eindex = self._quotes.index.get_loc(s.index[-1])

        self._index_time()

    def _make_chart(self) -> None:
        self._chart = CandleSticks(self.slice(), chart_size=self._chart_size)

    def _index_time(self) -> None:
        self._stime = self._quotes.index[self._sindex]
        self._etime = self._quotes.index[self._eindex]

    def forward(self) -> Optional[CandleSticks]:
        # if self._eindex + 1 >= len(self._quotes.index) or self._sindex + 1 >= self._eindex:
        if self._eindex + 1 >= len(self._quotes) or self._sindex + 1 >= self._eindex:
            return None

        self._sindex += 1
        self._eindex += 1

        self._index_time()
        self._make_chart()

        return self.chart()

    def backward(self) -> Optional[CandleSticks]:
        if self._sindex - 1 <= 0 or self._eindex - 1 <= self._sindex:
            return None

        self._sindex -= 1
        self._eindex -= 1

        self._index_time()
        self._make_chart()

        return self.chart()
