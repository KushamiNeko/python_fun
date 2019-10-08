import unittest

from fun.trading.trade import FuturesTrade
from fun.trading.transaction import FuturesTransaction


class TestFuturesTrade(unittest.TestCase):
    def test_init_invalid(self):

        tables = [
            {"orders": []},
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "short",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
        ]

        for table in tables:
            with self.assertRaises(ValueError):
                orders = [
                    FuturesTransaction.from_entity(order) for order in table["orders"]
                ]

                FuturesTrade(orders)

    def test_long_gain_succeed(self):

        tables = [
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10100",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": -50000,
                    "average_close": 50500,
                    "pl_dollar": 497,
                    "pl_percent": 0.994,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "2",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "2",
                        "price": "10100",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": -100000,
                    "average_close": 101000,
                    "pl_dollar": 994,
                    "pl_percent": 0.994,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "long",
                        "quantity": "1",
                        "price": "2722.75",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "es",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "2742",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "es",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "2776.25",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "1",
                        "price": "2777",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": -273237.5,
                    "average_close": 277662.5,
                    "pl_dollar": 4419,
                    "pl_percent": 1.617274349,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "long",
                        "quantity": "1",
                        "price": "2722.75",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "es",
                        "operation": "increase",
                        "quantity": "2",
                        "price": "2742",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "es",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "2776.25",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "2",
                        "price": "2777",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": -410337.5,
                    "average_close": 416512.5,
                    "pl_dollar": 6166,
                    "pl_percent": 1.502665489,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10050",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "2",
                        "price": "10100",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": -100250,
                    "average_close": 101000,
                    "pl_dollar": 744,
                    "pl_percent": 0.742145,
                },
            },
        ]

        for table in tables:
            orders = [
                FuturesTransaction.from_entity(order) for order in table["orders"]
            ]

            trade = FuturesTrade(orders)

            self.assertEqual(trade.symbol, table["expected"]["symbol"])
            self.assertEqual(trade.operation, table["expected"]["operation"])
            self.assertEqual(
                trade.open_time.strftime("%Y-%m-%d"), table["expected"]["open_time"]
            )
            self.assertEqual(
                trade.close_time.strftime("%Y-%m-%d"), table["expected"]["close_time"]
            )

            self.assertAlmostEqual(
                trade.average_open, table["expected"]["average_open"]
            )
            self.assertAlmostEqual(
                trade.average_close, table["expected"]["average_close"]
            )
            self.assertAlmostEqual(trade.pl_dollar, table["expected"]["pl_dollar"])
            self.assertAlmostEqual(
                trade.pl_percent, table["expected"]["pl_percent"], places=6
            )

    def test_long_stop_loss_succeed(self):

        tables = [
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "1",
                        "price": "9900",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": -50000,
                    "average_close": 49500,
                    "pl_dollar": -503,
                    "pl_percent": -1.006,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "2",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "2",
                        "price": "9900",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": -100000,
                    "average_close": 99000,
                    "pl_dollar": -1006,
                    "pl_percent": -1.006,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "long",
                        "quantity": "1",
                        "price": "2722.75",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "es",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "2742",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "es",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "2725.5",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "1",
                        "price": "2722",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": -273237.5,
                    "average_close": 272375,
                    "pl_dollar": -868.5,
                    "pl_percent": -0.317855346,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "long",
                        "quantity": "1",
                        "price": "2722.75",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "es",
                        "operation": "increase",
                        "quantity": "2",
                        "price": "2742",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "es",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "2725.5",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "2",
                        "price": "2722",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": -410337.5,
                    "average_close": 408475,
                    "pl_dollar": -1871.5,
                    "pl_percent": -0.456087976,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10050",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "2",
                        "price": "9925",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "long",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": -100250,
                    "average_close": 99250,
                    "pl_dollar": -1006,
                    "pl_percent": -1.003491,
                },
            },
        ]

        for table in tables:
            orders = [
                FuturesTransaction.from_entity(order) for order in table["orders"]
            ]

            trade = FuturesTrade(orders)

            self.assertEqual(trade.symbol, table["expected"]["symbol"])
            self.assertEqual(trade.operation, table["expected"]["operation"])
            self.assertEqual(
                trade.open_time.strftime("%Y-%m-%d"), table["expected"]["open_time"]
            )
            self.assertEqual(
                trade.close_time.strftime("%Y-%m-%d"), table["expected"]["close_time"]
            )

            self.assertAlmostEqual(
                trade.average_open, table["expected"]["average_open"]
            )
            self.assertAlmostEqual(
                trade.average_close, table["expected"]["average_close"]
            )
            self.assertAlmostEqual(trade.pl_dollar, table["expected"]["pl_dollar"])
            self.assertAlmostEqual(
                trade.pl_percent, table["expected"]["pl_percent"], places=6
            )

    def test_short_gain_succeed(self):

        tables = [
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "1",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "1",
                        "price": "73.05",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": 74400,
                    "average_close": -73050,
                    "pl_dollar": 1347,
                    "pl_percent": 1.810483871,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "2",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "2",
                        "price": "73.05",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": 148800,
                    "average_close": -146100,
                    "pl_dollar": 2694,
                    "pl_percent": 1.810483871,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "1",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "cl",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "73.05",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "53.81",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "1",
                        "price": "46.53",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": 147450,
                    "average_close": -100340,
                    "pl_dollar": 47104,
                    "pl_percent": 31.94574432,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "1",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "cl",
                        "operation": "increase",
                        "quantity": "2",
                        "price": "73.05",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "53.81",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "2",
                        "price": "46.53",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": 220500,
                    "average_close": -146870,
                    "pl_dollar": 73621,
                    "pl_percent": 33.388208617,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "short",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10050",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "2",
                        "price": "8020",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": 100250,
                    "average_close": -80200,
                    "pl_dollar": 20044,
                    "pl_percent": 19.994015,
                },
            },
        ]

        for table in tables:
            orders = [
                FuturesTransaction.from_entity(order) for order in table["orders"]
            ]

            trade = FuturesTrade(orders)

            self.assertEqual(trade.symbol, table["expected"]["symbol"])
            self.assertEqual(trade.operation, table["expected"]["operation"])
            self.assertEqual(
                trade.open_time.strftime("%Y-%m-%d"), table["expected"]["open_time"]
            )
            self.assertEqual(
                trade.close_time.strftime("%Y-%m-%d"), table["expected"]["close_time"]
            )

            self.assertAlmostEqual(
                trade.average_open, table["expected"]["average_open"]
            )
            self.assertAlmostEqual(
                trade.average_close, table["expected"]["average_close"]
            )
            self.assertAlmostEqual(trade.pl_dollar, table["expected"]["pl_dollar"])
            self.assertAlmostEqual(
                trade.pl_percent, table["expected"]["pl_percent"], places=6
            )

    def test_short_stop_loss_succeed(self):

        tables = [
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "1",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "1",
                        "price": "75.15",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": 74400,
                    "average_close": -75150,
                    "pl_dollar": -753,
                    "pl_percent": -1.012096774,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "2",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "2",
                        "price": "75.15",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": 148800,
                    "average_close": -150300,
                    "pl_dollar": -1506,
                    "pl_percent": -1.012097,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "1",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "cl",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "73.05",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "75.1",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "1",
                        "price": "73.8",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": 147450.0,
                    "average_close": -148900.0,
                    "pl_dollar": -1456.0,
                    "pl_percent": -0.987453,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "cl",
                        "operation": "short",
                        "quantity": "1",
                        "price": "74.4",
                        "note": "",
                    },
                    {
                        "time": "2019-03-09",
                        "symbol": "cl",
                        "operation": "increase",
                        "quantity": "2",
                        "price": "73.05",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "cl",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "75.1",
                        "note": "",
                    },
                    {
                        "time": "2019-03-18",
                        "symbol": "cl",
                        "operation": "close",
                        "quantity": "2",
                        "price": "73.8",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-18",
                    "average_open": 220500.0,
                    "average_close": -222700.0,
                    "pl_dollar": -2209.0,
                    "pl_percent": -1.001814,
                },
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "short",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10050",
                        "note": "",
                    },
                    {
                        "time": "2019-03-15",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "2",
                        "price": "10125",
                        "note": "",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "short",
                    "open_time": "2019-03-08",
                    "close_time": "2019-03-15",
                    "average_open": 100250,
                    "average_close": -101250,
                    "pl_dollar": -1006,
                    "pl_percent": -1.003491,
                },
            },
        ]

        for table in tables:
            orders = [
                FuturesTransaction.from_entity(order) for order in table["orders"]
            ]

            trade = FuturesTrade(orders)

            self.assertEqual(trade.symbol, table["expected"]["symbol"])
            self.assertEqual(trade.operation, table["expected"]["operation"])
            self.assertEqual(
                trade.open_time.strftime("%Y-%m-%d"), table["expected"]["open_time"]
            )
            self.assertEqual(
                trade.close_time.strftime("%Y-%m-%d"), table["expected"]["close_time"]
            )

            self.assertAlmostEqual(
                trade.average_open, table["expected"]["average_open"]
            )
            self.assertAlmostEqual(
                trade.average_close, table["expected"]["average_close"]
            )
            self.assertAlmostEqual(trade.pl_dollar, table["expected"]["pl_dollar"])
            self.assertAlmostEqual(
                trade.pl_percent, table["expected"]["pl_percent"], places=6
            )

    def test_quantity_mismatch(self):

        tables = [
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "2",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "short",
                        "quantity": "2",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
        ]

        for table in tables:
            with self.assertRaises(ValueError):
                orders = [
                    FuturesTransaction.from_entity(order) for order in table["orders"]
                ]

                FuturesTrade(orders)

    def test_symbol_mismatch(self):

        tables = [
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ym",
                        "operation": "long",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "short",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "short",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "increase",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "2",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "time": "2019-03-08",
                        "symbol": "ty",
                        "operation": "short",
                        "quantity": "2",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "decrease",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                    {
                        "time": "2019-03-08",
                        "symbol": "es",
                        "operation": "close",
                        "quantity": "1",
                        "price": "10000",
                        "note": "",
                    },
                ]
            },
        ]

        for table in tables:
            with self.assertRaises(ValueError):
                orders = [
                    FuturesTransaction.from_entity(order) for order in table["orders"]
                ]

                FuturesTrade(orders)
