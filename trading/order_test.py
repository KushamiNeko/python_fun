import time
import unittest
from datetime import datetime

from fun.trading.order import TransactionOrder
from fun.utils.testing import parameterized


class TestTransactionOrder(unittest.TestCase):
    @parameterized(
        [
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "symbol": "ES",
                    "operation": "-",
                    "leverage": 10,
                    "price": 2722,
                },
                "expected": {
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 10,
                    "price": 2722,
                },
            },
            {
                "inputs": {
                    "symbol": "Es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "symbol": "eS",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
                "expected": {
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
                "expected": {
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
            },
        ]
    )
    def test_new_order_succeed(self, inputs, expected):
        t = TransactionOrder(
            symbol=inputs["symbol"],
            operation=inputs["operation"],
            leverage=inputs["leverage"],
            price=inputs["price"],
        )

        self.assertEqual(expected["symbol"], t.symbol())
        self.assertEqual(expected["operation"], t.operation())
        self.assertEqual(expected["leverage"], t.leverage())
        self.assertEqual(expected["price"], t.price())

    @parameterized(
        [
            {
                "inputs": {
                    "symbol": "",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "[\\]",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "a123",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "hello",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "\\",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "123",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 0,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": -1,
                    "price": 2722.75,
                }
            },
            {"inputs": {"symbol": "es", "operation": "+", "leverage": 1, "price": 0,}},
            {"inputs": {"symbol": "es", "operation": "+", "leverage": 1, "price": -1,}},
        ]
    )
    def test_new_order_invalid(self, inputs):
        with self.assertRaises(ValueError):
            TransactionOrder(
                symbol=inputs["symbol"],
                operation=inputs["operation"],
                leverage=inputs["leverage"],
                price=inputs["price"],
            )

    @parameterized(
        [
            {
                "inputs": {
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                },
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                },
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
        ]
    )
    def test_futures_order_from_entity_succeed(self, inputs, expected):
        t = TransactionOrder.from_entity(inputs)

        self.assertEqual(expected["symbol"], t.symbol())
        self.assertEqual(expected["operation"], t.operation())
        self.assertEqual(expected["leverage"], t.leverage())
        self.assertEqual(expected["price"], t.price())


    def test_futures_transaction_to_entity_succeed(self):
        t = TransactionOrder(
            symbol="es",
            operation="+",
            leverage=1,
            price=2722.75,
        )

        nt = TransactionOrder.from_entity(t.to_entity())

        self.assertEqual(nt.symbol(), t.symbol())
        self.assertEqual(nt.operation(), t.operation())
        self.assertEqual(nt.leverage(), t.leverage())
        self.assertEqual(nt.price(), t.price())

    @parameterized(
        [
            {
                "inputs": {
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                }
            },
            {
                "inputs": {
                    "symbol": "ES",
                    "leverage": "1",
                    "price": "2722.75",
                }
            },
            {
                "inputs": {
                    "symbol": "ES",
                    "operation": "+",
                    "price": "2722.75",
                }
            },
            {
                "inputs": {
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                }
            },
        ]
    )
    def test_order_from_entity_missing_key(self, inputs):
        with self.assertRaises(KeyError):
            TransactionOrder.from_entity(inputs)


if __name__ == "__main__":
    unittest.main()
