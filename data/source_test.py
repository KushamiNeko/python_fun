import unittest
import os

from fun.data.source import Yahoo, StockCharts, InvestingCom
from fun.data.barchart import Barchart
from fun.data.continuous import Contract

from datetime import datetime

from utils import pretty, colors


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
                    pretty.color_print(colors.PAPER_AMBER_300, f"empty file: {src}")
                    continue

            symbol = os.path.splitext(f)[0]

            df = source.read(self._start, self._end, symbol, "d")
            self.assertNotEqual(len(df.index), 0)

            self.assertFalse(df.isna().any(axis=1).any())
            self.assertFalse((df.index.hour != 0).any())

    def test_yahoo(self):
        root = os.path.join(self._root(), "yahoo")
        self._loop_files(root, Yahoo())

    def test_stockcharts(self):
        root = os.path.join(self._root(), "stockcharts")
        self._loop_files(root, StockCharts())

    def test_investing(self):
        root = os.path.join(self._root(), "investing.com")
        self._loop_files(root, InvestingCom())

    def test_barchart(self):
        root = os.path.join(self._root(), "barchart")
        self._loop_files(root, Barchart())

    def test_contract(self):
        source = Contract()

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

                df = source.read(self._start, self._end, symbol, "d")
                self.assertNotEqual(len(df.index), 0)

                self.assertFalse(df.isna().any(axis=1).any())


if __name__ == "__main__":
    unittest.main()
