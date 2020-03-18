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
            self.assertAlmostEqual(a, b)

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
                    "nominal_win_loss_ratio": 5,
                    "leveraged_win_loss_ratio": 5,
                    "nominal_adjusted_win_loss_ratio": 5,
                    "leveraged_adjusted_win_loss_ratio": 5,
                    "nominal_expected_value": 0.02,
                    "leveraged_expected_value": 0.02,
                },
            },
            {
                "trades": [
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
                            "price": 105,
                        },
                    ],
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
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
                    "nominal_win_loss_ratio": 5,
                    "leveraged_win_loss_ratio": 5,
                    "nominal_adjusted_win_loss_ratio": 5,
                    "leveraged_adjusted_win_loss_ratio": 5,
                    "nominal_expected_value": 0.02,
                    "leveraged_expected_value": 0.04,
                },
            },
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
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 101.5,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 105,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
                            "price": 106.5,
                        },
                    ],
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 99,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
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
                    "nominal_win_loss_ratio": 3.300330033,
                    "leveraged_win_loss_ratio": 4.950495,
                    "nominal_adjusted_win_loss_ratio": 3.300330033,
                    "leveraged_adjusted_win_loss_ratio": 4.950495,
                    "nominal_expected_value": 0.017252475,
                    "leveraged_expected_value": 0.059257425,
                },
            },
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
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 101.5,
                        },
                        # 101
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 105,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
                            "price": 106.5,
                        },
                        # 106
                    ],
                    # 0.04950495
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 102,
                        },
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
                        },
                        # 100
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 90,
                        },
                        # 90
                    ],
                    # 0.1
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 102,
                        },
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
                        },
                        # 100
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 94,
                        },
                        # 94
                    ],
                    # 0.06
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        # 100
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 99,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
                        },
                        # 98.5
                    ],
                    # -0.015
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 101,
                        },
                    ],
                    # -0.01
                ],
                "expect": {
                    "total_trades": 5,
                    "number_of_winners": 3,
                    "number_of_losers": 2,
                    "batting_average": 0.6,
                    "batting_average_long": 0.5,
                    "batting_average_short": 0.666666667,
                    "nominal_win_loss_ratio": 5.586798667,
                    "leveraged_win_loss_ratio": 7.808580833,
                    "nominal_adjusted_win_loss_ratio": 8.380198,
                    "leveraged_adjusted_win_loss_ratio": 11.71287125,
                    "nominal_expected_value": 0.03690099,
                    "leveraged_expected_value": 0.08570297,
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

        self._assert_with_nan(
            stat.nominal_win_loss_ratio(), expect["nominal_win_loss_ratio"]
        )

        self._assert_with_nan(
            stat.leveraged_win_loss_ratio(), expect["leveraged_win_loss_ratio"]
        )

        self._assert_with_nan(
            stat.nominal_adjusted_win_loss_ratio(),
            expect["nominal_adjusted_win_loss_ratio"],
        )

        self._assert_with_nan(
            stat.leveraged_adjusted_win_loss_ratio(),
            expect["leveraged_adjusted_win_loss_ratio"],
        )

        self._assert_with_nan(
            stat.nominal_expected_value(), expect["nominal_expected_value"]
        )

        self._assert_with_nan(
            stat.leveraged_expected_value(), expect["leveraged_expected_value"]
        )


if __name__ == "__main__":
    unittest.main()
