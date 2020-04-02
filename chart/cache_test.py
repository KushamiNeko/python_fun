import unittest
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
                # "rolling": LastNTradingDays(offset=4, adjustment_method=RATIO),
            },
            {
                # forward None
                "exstart": "20180101",
                "exend": "20200101",
                "start": "20190101",
                "end": datetime.now().strftime("%Y%m%d"),
                "symbol": "es",
                "frequency": DAILY,
                # "rolling": LastNTradingDays(offset=4, adjustment_method=RATIO),
            },
            {
                # backward None
                "exstart": "20180101",
                "exend": "20200101",
                "start": "20170101",
                "end": "20200101",
                "symbol": "es",
                "frequency": DAILY,
                # "rolling": LastNTradingDays(offset=4, adjustment_method=RATIO),
            },
            {
                "exstart": "20020101",
                "exend": "20080101",
                "start": "20030101",
                "end": "20070101",
                "symbol": "es",
                "frequency": WEEKLY,
                # "rolling": LastNTradingDays(offset=4, adjustment_method=RATIO),
            },
            {
                # forward None
                "exstart": "20150101",
                "exend": "20200101",
                "start": "20160101",
                "end": datetime.now().strftime("%Y%m%d"),
                "symbol": "es",
                "frequency": WEEKLY,
                # "rolling": LastNTradingDays(offset=4, adjustment_method=RATIO),
            },
            {
                # backward None
                "exstart": "20150101",
                "exend": "20200101",
                "start": "20140101",
                "end": "20180101",
                "symbol": "es",
                "frequency": WEEKLY,
                # "rolling": LastNTradingDays(offset=4, adjustment_method=RATIO),
            },
        ]
    )
    def test_in_range(self, exstart, exend, start, end, symbol, frequency):
        c = ContinuousContract()

        exs = datetime.strptime(exstart, "%Y%m%d")
        exe = datetime.strptime(exend, "%Y%m%d")

        s = datetime.strptime(start, "%Y%m%d")
        e = datetime.strptime(end, "%Y%m%d")

        df = c.read(exs, exe, symbol, frequency)
        columns = df.columns

        original = df.copy()

        cache = QuotesCache(
            df,
            s,
            e,
            chart_factory=lambda quotes: CandleSticks(quotes, chart_size=MEDIUM_CHART),
        )

        self.assertLessEqual(cache.exstime(), exs)
        self.assertGreaterEqual(cache.exetime(), exe)

        self.assertGreaterEqual(cache.stime(), s)
        self.assertLessEqual(cache.etime(), e)

        self.assertGreaterEqual(cache.sindex(), df.index.get_loc(cache.stime()))
        self.assertLessEqual(cache.eindex(), df.index.get_loc(cache.etime()))

        self.assertTrue(original.eq(df.loc[:, columns]).all(axis=1).all())

        ################################

        cexs = cache.exstime()
        cexe = cache.exetime()

        cs = cache.stime()
        ce = cache.etime()

        csi = cache.sindex()
        cei = cache.eindex()

        cache.forward()

        self.assertEqual(cache.exstime(), cexs)
        self.assertEqual(cache.exetime(), cexe)

        if ce < cexe and cs < ce:
            self.assertGreater(cache.stime(), cs)
            self.assertGreater(cache.etime(), ce)

            self.assertGreater(cache.sindex(), csi)
            self.assertGreater(cache.eindex(), cei)
        else:
            self.assertEqual(cache.stime(), cs)
            self.assertEqual(cache.etime(), ce)

            self.assertEqual(cache.sindex(), csi)
            self.assertEqual(cache.eindex(), cei)

        self.assertTrue(original.eq(df.loc[:, columns]).all(axis=1).all())

        # ################################
        if ce < cexe and cs < ce:
            cache.backward()

            self.assertEqual(cache.exstime(), cexs)
            self.assertEqual(cache.exetime(), cexe)

            self.assertEqual(cache.stime(), cs)
            self.assertEqual(cache.etime(), ce)

            self.assertEqual(cache.sindex(), csi)
            self.assertEqual(cache.eindex(), cei)

            self.assertTrue(original.eq(df.loc[:, columns]).all(axis=1).all())
        # ################################

        cexs = cache.exstime()
        cexe = cache.exetime()

        cs = cache.stime()
        ce = cache.etime()

        csi = cache.sindex()
        cei = cache.eindex()

        cache.backward()

        self.assertEqual(cache.exstime(), cexs)
        self.assertEqual(cache.exetime(), cexe)

        if cs > cexs and ce > cs:
            self.assertLess(cache.stime(), cs)
            self.assertLess(cache.etime(), ce)

            self.assertLess(cache.sindex(), csi)
            self.assertLess(cache.eindex(), cei)
        else:
            self.assertEqual(cache.stime(), cs)
            self.assertEqual(cache.etime(), ce)

            self.assertEqual(cache.sindex(), csi)
            self.assertEqual(cache.eindex(), cei)

        self.assertTrue(original.eq(df.loc[:, columns]).all(axis=1).all())


if __name__ == "__main__":
    unittest.main()
