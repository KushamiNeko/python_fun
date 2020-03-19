import unittest
import io
from datetime import datetime

from fun.chart.cache import QuotesCache
from fun.chart.base import MEDIUM_CHART
from fun.chart.static import CandleSticks
from fun.data.source import DAILY, WEEKLY
from fun.futures.continuous import ContinuousContract
from fun.futures.rolling import RATIO, LastNTradingDays
from fun.utils.testing import parameterized


class TestQuotesCache(unittest.TestCase):
    @parameterized(
        [
            {
                "exstart": "20180101",
                "exend": "20200101",
                "start": "20180601",
                "end": "20190601",
                "symbol": "es",
                "frequency": DAILY,
                "rolling": LastNTradingDays(offset=4, adjustment_method=RATIO),
            },
        ]
    )
    def test(self, exstart, exend, start, end, symbol, frequency, rolling):
        c = ContinuousContract()

        exs = datetime.strptime(exstart, "%Y%m%d")
        exe = datetime.strptime(exend, "%Y%m%d")

        s = datetime.strptime(start, "%Y%m%d")
        e = datetime.strptime(end, "%Y%m%d")

        df = c.read(exs, exe, symbol, frequency, rolling)
        columns = df.columns

        original = df.copy()

        cache = QuotesCache(df, s, e)

        self.assertLessEqual(cache.exstime(), exs)
        self.assertGreaterEqual(cache.exetime(), exe)

        self.assertGreaterEqual(cache.stime(), s)
        self.assertLessEqual(cache.etime(), e)

        self.assertTrue(original.eq(df.loc[:, columns]).all(axis=1).all())

    # def slice(self) -> pd.DataFrame:
    # return self._quotes.loc[self._stime : self._etime]

    # def chart(self) -> CandleSticks:
    # return self._chart

    # def time_slice(self, stime: datetime, etime: datetime) -> None:
    # s = self._quotes.loc[stime:etime]

    # self._sindex = self._quotes.index.get_loc(s.index[0])
    # self._eindex = self._quotes.index.get_loc(s.index[-1])

    # self._index_time()

    # def _make_chart(self) -> None:
    # # self._chart = StaticChart(self.slice, chart_size="m")
    # self._chart = CandleSticks(self.slice, chart_size=MEDIUM_CHART)

    # def _index_time(self) -> None:
    # self._stime = self._quotes.index[self._sindex]
    # self._etime = self._quotes.index[self._eindex]

    # def forward(self) -> Optional[CandleSticks]:
    # # if self._eindex + 1 >= len(self._quotes.index) or self._sindex + 1 >= self._eindex:
    # if self._eindex + 1 >= len(self._quotes) or self._sindex + 1 >= self._eindex:
    # return None

    # self._sindex += 1
    # self._eindex += 1

    # self._index_time()
    # self._make_chart()

    # return self.chart()

    # def backward(self) -> Optional[CandleSticks]:
    # if self._sindex - 1 <= 0 or self._eindex - 1 <= self._sindex:
    # return None

    # self._sindex -= 1
    # self._eindex -= 1

    # self._index_time()
    # self._make_chart()

    # return self.chart()


if __name__ == "__main__":
    unittest.main()
