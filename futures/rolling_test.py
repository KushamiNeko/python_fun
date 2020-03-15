import unittest
from datetime import datetime

from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    Contract,
)
from fun.futures.rolling import (
    first_of_month,
    last_n_trading_days,
    volume_and_open_interest,
)
from fun.utils.testing import parameterized


class TestRolling(unittest.TestCase):
    @parameterized(
        [
            {
                "front_code": "esz19",
                "back_code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": lambda front, back: last_n_trading_days(front, back, 4),
                "expect_rolling": "20191217",
            },
            {
                "front_code": "clz19",
                "back_code": "clf20",
                "months": ALL_CONTRACT_MONTHS,
                "rolling_func": lambda front, back: last_n_trading_days(front, back, 4),
                "expect_rolling": "20191115",
            },
            {
                "front_code": "clj09",
                "back_code": "clk09",
                "months": ALL_CONTRACT_MONTHS,
                "rolling_func": lambda front, back: last_n_trading_days(front, back, 4),
                "expect_rolling": "20090317",
            },
            {
                "front_code": "gcj19",
                "back_code": "gcm19",
                "months": EVEN_CONTRACT_MONTHS,
                "rolling_func": lambda front, back: last_n_trading_days(front, back, 4),
                "expect_rolling": "20190423",
            },
            {
                "front_code": "esh00",
                "back_code": "esm00",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": lambda front, back: last_n_trading_days(front, back, 4),
                "expect_rolling": "20000314",
            },
            {
                "front_code": "esz99",
                "back_code": "esh00",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": first_of_month,
                "expect_rolling": "19991201",
            },
            {
                "front_code": "esh10",
                "back_code": "esm10",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": first_of_month,
                "expect_rolling": "20100301",
            },
            {
                "front_code": "esm99",
                "back_code": "esu99",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": first_of_month,
                "expect_rolling": "19990601",
            },
            {
                "front_code": "clf00",
                "back_code": "clg00",
                "months": ALL_CONTRACT_MONTHS,
                "rolling_func": first_of_month,
                "expect_rolling": "19991201",
            },
            {
                "front_code": "gcj01",
                "back_code": "gcm01",
                "months": EVEN_CONTRACT_MONTHS,
                "rolling_func": first_of_month,
                "expect_rolling": "20010402",
            },
            {
                "front_code": "esh19",
                "back_code": "esm19",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": volume_and_open_interest,
                "expect_rolling": "20190311",
            },
            {
                "front_code": "esz09",
                "back_code": "esh10",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": volume_and_open_interest,
                "expect_rolling": "20091214",
            },
            {
                "front_code": "gcg10",
                "back_code": "gcj10",
                "months": EVEN_CONTRACT_MONTHS,
                "rolling_func": volume_and_open_interest,
                "expect_rolling": "20100128",
            },
            {
                "front_code": "clf00",
                "back_code": "clg00",
                "months": ALL_CONTRACT_MONTHS,
                "rolling_func": volume_and_open_interest,
                "expect_rolling": "19991201",
            },
            {
                "front_code": "esh00",
                "back_code": "esm00",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "rolling_func": lambda front, back: volume_and_open_interest(
                    front,
                    back,
                    backup_rolling=lambda front, back: last_n_trading_days(
                        front, back, 4
                    ),
                ),
                "expect_rolling": "20000314",
            },
        ]
    )
    def test_rolling(self, front_code, back_code, months, rolling_func, expect_rolling):
        f = Contract(code=front_code, months=months, fmt="barchart", read_data=True,)
        b = Contract(code=back_code, months=months, fmt="barchart", read_data=True,)
        self.assertEqual(
            rolling_func(f, b), datetime.strptime(expect_rolling, "%Y%m%d")
        )


if __name__ == "__main__":
    unittest.main()
