import io
import unittest
from datetime import datetime

from fun.chart.base import MEDIUM_CHART
from fun.chart.static import CandleSticks
from fun.data.source import DAILY, WEEKLY
from fun.futures.continuous import ContinuousContract
from fun.futures.rolling import RATIO, LastNTradingDays
from fun.utils.testing import parameterized


class TestStaticCandleSticks(unittest.TestCase):
    @parameterized(
        [
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "freqneucy": DAILY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19980101",
                "end": "19990101",
                "symbol": "es",
                "freqneucy": DAILY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19970101",
                "end": "19980101",
                "symbol": "es",
                "freqneucy": DAILY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19960101",
                "end": "19970101",
                "symbol": "es",
                "freqneucy": DAILY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": ValueError,
            },
            {
                "start": "19950101",
                "end": "19960101",
                "symbol": "es",
                "freqneucy": DAILY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": ValueError,
            },
            {
                "start": "20160101",
                "end": "20200101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19950101",
                "end": "19990101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19940101",
                "end": "19980101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19930101",
                "end": "19970101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": ValueError,
            },
            {
                "start": "19920101",
                "end": "19960101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "make_slice": True,
                "error": ValueError,
            },
        ]
    )
    def test_plot(
        self, start, end, symbol, freqneucy, rolling_method, make_slice, error
    ):
        c = ContinuousContract()

        s = datetime.strptime(start, "%Y%m%d")
        e = datetime.strptime(end, "%Y%m%d")

        if error is not None:
            with self.assertRaises(error):
                c.read(s, e, symbol, freqneucy, rolling_method)

        else:
            df = c.read(s, e, symbol, freqneucy, rolling_method)

            if make_slice:
                df = df.loc[(df.index >= s) & (df.index <= e)]

            original = df.copy()

            buf = io.BytesIO()

            chart = CandleSticks(
                df.loc[(df.index >= s) & (df.index <= e)], chart_size=MEDIUM_CHART
            )

            chart.render(buf)

            self.assertTrue(original.eq(df).all(axis=1).all())


if __name__ == "__main__":
    unittest.main()
