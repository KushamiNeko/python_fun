import unittest
from datetime import datetime
from fun.futures.continuous import ContinuousContract
from fun.data.source import DAILY, FREQUENCY, WEEKLY, daily_to_weekly
from fun.futures.rolling import LastNTradingDays


class TestContinuousContract(unittest.TestCase):
    def test_read(self):
        c = ContinuousContract()
        df = c.read(
            datetime.strptime("20190101", "%Y%m%d"),
            datetime.strptime("20200101", "%Y%m%d"),
            "es",
            DAILY,
            rolling_method=LastNTradingDays(offset=4),
        )

        print(df)


if __name__ == "__main__":
    unittest.main()
