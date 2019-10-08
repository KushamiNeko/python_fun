import time
import unittest
from datetime import datetime

from fun.trading.transaction import FuturesTransaction


class TestFuturesTransaction(unittest.TestCase):
    def test_new_transaction_succeed(self):

        tables = [
            {
                "inputs": {
                    "dtime": datetime.strptime("2019-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "long",
                    "quantity": 1,
                    "price": 2722.75,
                    "note": "5 sma bounced off the 20 sma",
                },
                "expected": {
                    "dtime": datetime.strptime("2019-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "long",
                    "quantity": 1,
                    "price": 2722.75,
                    "note": "5 sma bounced off the 20 sma",
                },
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2019-03-10", "%Y-%m-%d"),
                    "symbol": "ES",
                    "operation": "short",
                    "quantity": 10,
                    "price": 2722,
                    "note": "5SMA BOUNCED OFF 20SMA",
                },
                "expected": {
                    "dtime": datetime.strptime("2019-03-10", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "short",
                    "quantity": 10,
                    "price": 2722,
                    "note": "5SMA BOUNCED OFF 20SMA",
                },
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2021-03-13", "%Y-%m-%d"),
                    "symbol": "Es",
                    "operation": "increase",
                    "quantity": 1,
                    "price": 2722.75,
                    "note": "5 SMA bounced off the 20 SMA",
                },
                "expected": {
                    "dtime": datetime.strptime("2021-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "increase",
                    "quantity": 1,
                    "price": 2722.75,
                    "note": "5 SMA bounced off the 20 SMA",
                },
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2019-01-13", "%Y-%m-%d"),
                    "symbol": "eS",
                    "operation": "decrease",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "",
                },
                "expected": {
                    "dtime": datetime.strptime("2019-01-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "decrease",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "",
                },
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "close",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                },
                "expected": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "close",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                },
            },
        ]

        for table in tables:
            t = FuturesTransaction(
                dtime=table["inputs"]["dtime"],
                symbol=table["inputs"]["symbol"],
                operation=table["inputs"]["operation"],
                quantity=table["inputs"]["quantity"],
                price=table["inputs"]["price"],
                note=table["inputs"]["note"],
            )

            self.assertEqual(
                table["expected"]["dtime"].strftime("%Y-%m-%d"),
                t.time.strftime("%Y-%m-%d"),
            )
            self.assertEqual(table["expected"]["symbol"], t.symbol)
            self.assertEqual(table["expected"]["operation"], t.operation)
            self.assertEqual(table["expected"]["quantity"], t.quantity)
            self.assertEqual(table["expected"]["price"], t.price)
            self.assertEqual(t.total_cost, t.quantity * t.price)
            self.assertEqual(table["expected"]["note"], t.note)

            self.assertNotEqual("", t.index)
            self.assertLess(0, t.time_stamp)

    def test_new_transaction_invalid(self):

        tables = [
            {
                "inputs": {
                    "dtime": -1,
                    "symbol": "es",
                    "operation": "long",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "",
                    "operation": "short",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "[\\]",
                    "operation": "short",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "a123",
                    "operation": "short",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "hello",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "\\",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "123",
                    "quantity": 2,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "increase",
                    "quantity": 0,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "increase",
                    "quantity": -1,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "increase",
                    "quantity": 1.5,
                    "price": 2722.75,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "increase",
                    "quantity": 1,
                    "price": 0,
                    "note": "hello",
                }
            },
            {
                "inputs": {
                    "dtime": datetime.strptime("2016-03-13", "%Y-%m-%d"),
                    "symbol": "es",
                    "operation": "increase",
                    "quantity": 1,
                    "price": -1,
                    "note": "hello",
                }
            },
        ]

        for table in tables:
            with self.assertRaises(ValueError):
                FuturesTransaction(
                    dtime=table["inputs"]["dtime"],
                    symbol=table["inputs"]["symbol"],
                    operation=table["inputs"]["operation"],
                    quantity=table["inputs"]["quantity"],
                    price=table["inputs"]["price"],
                    note=table["inputs"]["note"],
                )

    def test_futures_transaction_from_entity_succeed(self):

        tables = [
            {
                "inputs": {
                    "time": "2019-03-08",
                    "symbol": "ES",
                    "operation": "long",
                    "quantity": "1",
                    "price": "2722.75",
                    "note": "5SMA bounced off 20SMA",
                },
                "expected": {
                    "time": "2019-03-08",
                    "symbol": "es",
                    "operation": "long",
                    "quantity": 1,
                    "price": 2722.75,
                    "note": "5SMA bounced off 20SMA",
                },
            },
            {
                "inputs": {
                    "time": "2019-03-08",
                    "symbol": "ES",
                    "operation": "long",
                    "quantity": "1",
                    "price": "2722.75",
                },
                "expected": {
                    "time": "2019-03-08",
                    "symbol": "es",
                    "operation": "long",
                    "quantity": 1,
                    "price": 2722.75,
                    "note": "",
                },
            },
            {
                "inputs": {
                    "time": "2019-03-08",
                    "symbol": "ES",
                    "operation": "long",
                    "quantity": "1",
                    "price": "2722.75",
                    "note": "5SMA bounced off 20SMA",
                    "time_stamp": str(time.time()),
                },
                "expected": {
                    "time": "2019-03-08",
                    "symbol": "es",
                    "operation": "long",
                    "quantity": 1,
                    "price": 2722.75,
                    "note": "5SMA bounced off 20SMA",
                    "time_stamp": time.time(),
                },
            },
        ]

        for table in tables:
            t = FuturesTransaction.from_entity(table["inputs"])

            self.assertEqual(table["expected"]["time"], t.time.strftime("%Y-%m-%d"))
            self.assertEqual(table["expected"]["symbol"], t.symbol)
            self.assertEqual(table["expected"]["operation"], t.operation)
            self.assertEqual(table["expected"]["quantity"], t.quantity)
            self.assertEqual(table["expected"]["price"], t.price)
            self.assertEqual(t.total_cost, t.quantity * t.price)
            self.assertEqual(table["expected"]["note"], t.note)

            self.assertNotEqual("", t.index)
            self.assertLess(0, t.time_stamp)

    def test_futures_transaction_from_entity_time_stamp_sort_succeed(self):
        tf = FuturesTransaction.from_entity(
            {
                "time": "2019-03-08",
                "symbol": "ES",
                "operation": "long",
                "quantity": "1",
                "price": "2722.75",
                "note": "5SMA bounced off 20SMA",
                "time_stamp": str(time.time()),
            }
        )

        ts = FuturesTransaction.from_entity(
            {
                "time": "2019-03-08",
                "symbol": "ES",
                "operation": "increase",
                "quantity": "1",
                "price": "2722.75",
                "note": "5SMA bounced off 20SMA",
                "time_stamp": str(time.time()),
            }
        )

        self.assertNotEqual(0, tf.time_stamp)
        self.assertNotEqual(0, ts.time_stamp)
        self.assertNotEqual(tf.time_stamp, ts.time_stamp)
        self.assertLess(tf.time_stamp, ts.time_stamp)

    def test_futures_transaction_to_entity_succeed(self):
        t = FuturesTransaction(
            dtime=datetime.strptime("2019-10-04", "%Y-%m-%d"),
            symbol="ES",
            operation="long",
            quantity=1,
            price=2722.75,
            note="5SMA bounced off 20SMA",
        )

        nt = FuturesTransaction.from_entity(t.to_entity())

        self.assertEqual(nt.time, t.time)
        self.assertEqual(nt.symbol, t.symbol)
        self.assertEqual(nt.operation, t.operation)
        self.assertEqual(nt.quantity, t.quantity)
        self.assertEqual(nt.price, t.price)
        self.assertEqual(nt.note, t.note)
        self.assertEqual(nt.index, t.index)
        self.assertEqual(nt.time_stamp, t.time_stamp)

    def test_futures_transaction_from_entity_missing_key(self):

        tables = [
            {
                "inputs": {
                    "symbol": "ES",
                    "operation": "long",
                    "quantity": "1",
                    "price": "2722.75",
                    "note": "5SMA bounced off 20SMA",
                }
            },
            {
                "inputs": {
                    "time": "2019-10-04",
                    "operation": "long",
                    "quantity": "1",
                    "price": "2722.75",
                    "note": "5SMA bounced off 20SMA",
                }
            },
            {
                "inputs": {
                    "time": "2019-10-04",
                    "symbol": "ES",
                    "quantity": "1",
                    "price": "2722.75",
                    "note": "5SMA bounced off 20SMA",
                }
            },
            {
                "inputs": {
                    "time": "2019-10-04",
                    "symbol": "ES",
                    "operation": "long",
                    "price": "2722.75",
                    "note": "5SMA bounced off 20SMA",
                }
            },
            {
                "inputs": {
                    "time": "2019-10-04",
                    "symbol": "ES",
                    "operation": "long",
                    "quantity": "1",
                    "note": "5SMA bounced off 20SMA",
                }
            },
        ]

        for table in tables:
            with self.assertRaises(KeyError):
                FuturesTransaction.from_entity(table["inputs"])
