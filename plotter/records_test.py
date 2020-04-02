import unittest
from datetime import datetime

from fun.data.source import DAILY
from fun.futures.continuous import ContinuousContract
from fun.futures.rolling import RATIO, LastNTradingDays
from fun.plotter.records import LeverageRecords
from fun.trading.transaction import FuturesTransaction
from fun.utils.testing import parameterized


class TestLeverageRecords(unittest.TestCase):
    @parameterized(
        [
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "freqneucy": DAILY,
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "records": [
                    {
                        "datetime": "20190313",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": 1,
                        "price": 2722.75,
                    },
                    {
                        "datetime": "20190320",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": 1,
                        "price": 2722.75,
                    },
                    {
                        "datetime": "20190329",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": 1,
                        "price": 2722.75,
                    },
                    {
                        "datetime": "20190401",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": 1,
                        "price": 2722.75,
                    },
                    {
                        "datetime": "20190507",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": 2,
                        "price": 2722.75,
                    },
                    {
                        "datetime": "20190507",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": 1,
                        "price": 2722.75,
                    },
                    {
                        "datetime": "20190507",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": 1,
                        "price": 2722.75,
                    },
                ],
            },
        ]
    )
    def test_plot(self, start, end, symbol, freqneucy, rolling_method, records):
        pass
        # c = ContinuousContract()

        # s = datetime.strptime(start, "%Y%m%d")
        # e = datetime.strptime(end, "%Y%m%d")

        # df = c.read(s, e, symbol, freqneucy, rolling_method)

        # ts = [FuturesTransaction.from_entity(r) for r in records]

        # lr = LeverageRecords(df, ts)

        # lr.plot(None)
