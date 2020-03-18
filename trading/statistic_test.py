import unittest
import math

from fun.trading.statistic import Statistic
from fun.trading.trade import FuturesTrade
from fun.trading.transaction import FuturesTransaction
from fun.utils.testing import parameterized


class TestStatistic(unittest.TestCase):
    def _assert_with_nan(self, a, b):
        if math.isnan(a) or math.isnan(b):
            self.assertTrue(math.isnan(a) and math.isnan(b))
        else:
            self.assertEqual(a, b)

    @parameterized(
        [
            {
                "trades": [
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 105,
                        },
                    ],
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 99,
                        },
                    ],
                ],
                "expect": {
                    "total_trades": 2,
                    "number_of_winners": 1,
                    "number_of_losers": 1,
                    "batting_average": 0.5,
                    "batting_average_long": 0.5,
                    "batting_average_short": math.nan,
                    # "nominal_win_loss_ratio": f"{self.nominal_win_loss_ratio():.{self._float_decimals}f}",
                    # "leveraged_win_loss_ratio": f"{self.leveraged_win_loss_ratio():.{self._float_decimals}f}",
                    # "nominal_adjusted_win_loss_ratio": f"{self.nominal_adjusted_win_loss_ratio():.{self._float_decimals}f}",
                    # "leveraged_adjusted_win_loss_ratio": f"{self.leveraged_adjusted_win_loss_ratio():.{self._float_decimals}f}",
                    # "nominal_expected_value": f"{self.nominal_expected_value():.{self._float_decimals}f}%",
                    # "leveraged_expected_value": f"{self.leveraged_expected_value():.{self._float_decimals}f}%",
                },
            },
        ]
    )
    def test_statistic(self, trades, expect):
        ts = [
            FuturesTrade([FuturesTransaction.from_entity(t) for t in trade])
            for trade in trades
        ]
        stat = Statistic(ts)

        self.assertEqual(stat.total_trades(), expect["total_trades"])
        self.assertEqual(stat.number_of_winners(), expect["number_of_winners"])
        self.assertEqual(stat.number_of_losers(), expect["number_of_losers"])

        self._assert_with_nan(stat.batting_average(), expect["batting_average"])
        self._assert_with_nan(
            stat.batting_average_long(), expect["batting_average_long"]
        )
        self._assert_with_nan(
            stat.batting_average_short(), expect["batting_average_short"]
        )

    # database = JsonInterface(testing=True)
    # context = Context(database)
    # _trades = None

    # @classmethod
    # def setUpClass(cls):
    # cls.context.login("TEST")

    # es_open_1 = FuturesTransaction(
    # date=20190308,
    # symbol="ES",
    # operation="+",
    # quantity=2,
    # contract_price=1000,
    # note="5SMA bounced off 20SMA",
    # )

    # es_close_1 = FuturesTransaction(
    # date=20190315,
    # symbol="ES",
    # operation="-",
    # quantity=2,
    # contract_price=2000,
    # note="losing strength",
    # )

    # cl_open_1 = FuturesTransaction(
    # date=20190510,
    # symbol="CL",
    # operation="-",
    # quantity=2,
    # contract_price=1000,
    # note="5SMA bounced off 20SMA",
    # )

    # cl_close_1 = FuturesTransaction(
    # date=20190601,
    # symbol="CL",
    # operation="+",
    # quantity=2,
    # contract_price=500,
    # note="break down",
    # )

    # rty_open_1 = FuturesTransaction(
    # date=20190510,
    # symbol="RTY",
    # operation="+",
    # quantity=2,
    # contract_price=1000,
    # note="5SMA bounced off 20SMA",
    # )

    # rty_close_1 = FuturesTransaction(
    # date=20190601,
    # symbol="RTY",
    # operation="-",
    # quantity=2,
    # contract_price=990,
    # note="break down",
    # )

    # gc_open_1 = FuturesTransaction(
    # date=20190510,
    # symbol="GC",
    # operation="-",
    # quantity=2,
    # contract_price=1000,
    # note="5SMA bounced off 20SMA",
    # )

    # gc_close_1 = FuturesTransaction(
    # date=20190601,
    # symbol="GC",
    # operation="+",
    # quantity=2,
    # contract_price=1005,
    # note="break down",
    # )

    # transactions = [
    # es_open_1,
    # es_close_1,
    # rty_open_1,
    # rty_close_1,
    # cl_open_1,
    # cl_close_1,
    # gc_open_1,
    # gc_close_1,
    # ]

    # trading = Trading(cls.context)
    # cls._trades = trading._process_trades(transactions)

    # def test_total_trades_succeed(self):
    # es_dollar = 2000 * FuturesContractSpecs.lookup_contract_unit("ES") - (
    # 4 * config.PER_CONTRACT_COMMISSION_FEE
    # )
    # cl_dollar = 1000 * FuturesContractSpecs.lookup_contract_unit("CL") - (
    # 4 * config.PER_CONTRACT_COMMISSION_FEE
    # )

    # rty_dollar = -20 * FuturesContractSpecs.lookup_contract_unit("RTY") - (
    # 4 * config.PER_CONTRACT_COMMISSION_FEE
    # )
    # gc_dollar = -10 * FuturesContractSpecs.lookup_contract_unit("GC") - (
    # 4 * config.PER_CONTRACT_COMMISSION_FEE
    # )

    # w_mean = (es_dollar + cl_dollar) / 2.0
    # l_mean = (rty_dollar + gc_dollar) / 2.0

    # statistic = Statistic(self._trades)

    # self.assertEqual(statistic.total_trades(), len(self._trades))
    # self.assertEqual(statistic.number_of_winners(), 2)
    # self.assertEqual(statistic.number_of_losers(), 2)
    # self.assertEqual(statistic.batting_average(), 0.5)

    # self.assertEqual(
    # statistic.win_loss_ratio(),
    # round(w_mean / abs(l_mean), config.FLOAT_DECIMALS),
    # )
    # self.assertEqual(
    # statistic.adjusted_win_loss_ratio(),
    # round((w_mean * 0.5) / (abs(l_mean) * 0.5), config.FLOAT_DECIMALS),
    # )
    # self.assertEqual(
    # statistic.expected_value(),
    # round((w_mean * 0.5) + (l_mean * 0.5), config.FLOAT_DECIMALS),
    # )
    # self.assertEqual(
    # statistic.kelly_criterion(),
    # round(
    # 0.5 - (0.5 / round(w_mean / abs(l_mean), config.FLOAT_DECIMALS)),
    # config.FLOAT_DECIMALS,
    # ),
    # )


if __name__ == "__main__":
    unittest.main()
