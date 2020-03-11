import unittest
import os

from source import Yahoo, StockCharts, InvestingCom

from datetime import datetime


class TestSource(unittest.TestCase):

    _time_fmt = "%Y%m%d"

    _start = datetime.strptime("20170101", _time_fmt)
    _end = datetime.strptime("20180101", _time_fmt)

    def _root(self):
        home = os.getenv("HOME")
        assert home is not None

        root = os.path.join(home, "Documents", "data_source")

        return root

    def _loop_files(self, root, source):
        for f in os.listdir(root):
            src = os.path.join(root, f)

            with open(src, "r") as fc:
                if len(fc.read().strip()) == 0:
                    continue

            symbol = os.path.splitext(f)[0]

            df = source.read(self._start, self._end, symbol, "d")
            self.assertNotEqual(len(df.index), 0)

            self.assertFalse(df.isna().any(axis=1).any())

    def test_yahoo(self):
        root = os.path.join(self._root(), "yahoo")
        self._loop_files(root, Yahoo())

    def test_stockcharts(self):
        root = os.path.join(self._root(), "stockcharts")
        self._loop_files(root, StockCharts())

    def test_investing(self):
        root = os.path.join(self._root(), "investing.com")
        self._loop_files(root, InvestingCom())
