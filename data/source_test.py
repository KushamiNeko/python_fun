import unittest

import pandas as pd
import os

from fun.data.source import Yahoo, StockCharts, InvestingCom, DAILY, WEEKLY
from fun.data.barchart import Barchart, BarchartContract

from datetime import datetime

from fun.utils import pretty, colors


class TestSource(unittest.TestCase):

    _time_fmt = "%Y%m%d"

    _start = datetime.strptime("20170101", _time_fmt)
    _end = datetime.strptime("20180101", _time_fmt)

    def _root(self):
        home = os.getenv("HOME")
        assert home is not None

        root = os.path.join(home, "Documents", "data_source")

        return root

    def _loop_files(self, root, source, zero_exception=[]):
        for f in os.listdir(root):
            src = os.path.join(root, f)

            with open(src, "r") as fc:
                if len(fc.read().strip()) == 0:
                    pretty.color_print(colors.PAPER_AMBER_300, f"empty file: {src}")
                    continue

            symbol = os.path.splitext(f)[0]

            df = source.read(self._start, self._end, symbol, DAILY)
            self.assertNotEqual(len(df.index), 0)

            self.assertFalse(df.isna().any(axis=1).any())
            self.assertFalse((df.index.hour != 0).any())

            opens = df.loc[:, "open"]
            highs = df.loc[:, "high"]
            lows = df.loc[:, "low"]
            closes = df.loc[:, "close"]

            if symbol not in zero_exception:
                rows = df.loc[(opens <= 0) | (highs <= 0) | (lows <= 0) | (closes <= 0)]

                if len(rows) > 0:
                    pretty.color_print(
                        colors.PAPER_RED_400,
                        f"{symbol.upper()} contains 0 in open, high, low, or close",
                    )

                self.assertEqual(
                    len(rows), 0,
                )

    def test_daily_to_weekly(self):
        c = Yahoo()

        s = datetime.strptime("20180101", "%Y%m%d")
        e = datetime.strptime("20200101", "%Y%m%d")

        df = c.read(start=s, end=e, symbol="sml", frequency=WEEKLY)

        target = pd.read_csv(os.path.join(self._root(), "testing", "sml_w.csv"))

        target.drop("Adj Close", axis=1)

        cols = {k: k.lower() for k in target.columns}
        cols["Date"] = "timestamp"
        target = target.rename(columns=cols)

        target.loc[:, "timestamp"] = target.loc[:, "timestamp"].apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d"),
        )

        target = target.set_index("timestamp")

        columns = ["open", "high", "low", "close"]

        for i in df.index:
            if i in target.index:
                if i.to_pydatetime().year < 1996:
                    continue

                equals = (
                    target.loc[target.index == i, columns] == df.loc[i, columns]
                ).all(axis=1)

                assert len(equals) == 1

                equals = equals[0]
                self.assertTrue(equals)

    def test_yahoo(self):
        root = os.path.join(self._root(), "yahoo")
        self._loop_files(root, Yahoo())

    def test_stockcharts(self):
        root = os.path.join(self._root(), "stockcharts")
        self._loop_files(root, StockCharts(), zero_exception=["spxhilo", "ndxhilo"])

    def test_investing(self):
        root = os.path.join(self._root(), "investing.com")
        self._loop_files(root, InvestingCom())

    def test_barchart(self):
        root = os.path.join(self._root(), "barchart")
        self._loop_files(root, Barchart())

    def test_contract(self):
        source = BarchartContract()

        root = os.path.join(self._root(), "continuous")
        for f in os.listdir(os.path.join(self._root(), "continuous")):
            symbols = os.path.join(root, f)

            for f in os.listdir(symbols):
                src = os.path.join(symbols, f)

                with open(src, "r") as fc:
                    if len(fc.read().strip()) == 0:
                        pretty.color_print(colors.PAPER_AMBER_300, f"empty file: {src}")
                        continue

                symbol = os.path.splitext(f)[0]

                df = source.read(self._start, self._end, symbol, DAILY)
                self.assertNotEqual(len(df.index), 0)

                self.assertFalse(df.isna().any(axis=1).any())


if __name__ == "__main__":
    unittest.main()
