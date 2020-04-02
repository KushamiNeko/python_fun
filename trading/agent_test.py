import os
import unittest
from typing import cast
from datetime import datetime

from fun.trading.agent import TradingAgent
from fun.utils import colors, pretty
from fun.utils.jsondb import JsonDB
from fun.utils.testing import parameterized


class TestTradingAgent(unittest.TestCase):
    def _check_root(self, root):
        if not os.path.exists(root):
            os.makedirs(root)
        else:
            for f in os.listdir(root):
                pretty.color_print(
                    colors.PAPER_RED_500, f"removing file {os.path.join(root, f)}"
                )
                os.remove(os.path.join(root, f))

        self.assertTrue(os.path.exists(root))

    def _clean_root(self, root):
        for f in os.listdir(root):
            pretty.color_print(
                colors.PAPER_RED_500, f"removing file {os.path.join(root, f)}"
            )
            os.remove(os.path.join(root, f))

            self.assertFalse(os.path.exists(os.path.join(root, f)))

        pretty.color_print(colors.PAPER_RED_500, f"removing dir {root}")
        os.rmdir(root)

        self.assertFalse(os.path.exists(root))

    @parameterized(
        [
            {
                "user_name": "nonexist",
                "new_user": False,
                "error": ValueError,
                "expected": None,
            },
            {
                "user_name": "new",
                "new_user": True,
                "error": None,
                "expected": [{"name": "new", "uid": ""}],
            },
        ]
    )
    def test_init(self, user_name, new_user, error, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "agent",
        )

        self._check_root(root)

        if os.path.exists(os.path.join(root, "admin_user.json")):
            jsonDB = JsonDB(root)
            jsonDB.drop("admin", "user")

        if error is not None:
            with self.assertRaises(ValueError):
                TradingAgent(
                    root, user_name=user_name, new_user=new_user,
                )
        else:
            self.assertTrue(expected is not None)

            TradingAgent(
                root, user_name=user_name, new_user=new_user,
            )

            db = "admin"
            col = "user"

            self.assertTrue(os.path.exists(os.path.join(root, f"{db}_{col}.json")))

            jsonDB = JsonDB(root)
            results = jsonDB.find(db, col, query=None)

            if len(expected) == 0:
                self.assertIsNone(results)

            else:
                assert results is not None

                self.assertEqual(len(results), len(expected))

                for i in range(len(results)):
                    r = results[i]
                    e = expected[i]

                    for k in r.keys():
                        er = e.get(k, None)
                        if er != "":
                            self.assertEqual(r[k], e.get(k, None))
                        else:
                            self.assertNotEqual(r[k], "")

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
        ]
    )
    def test_read_trades(self, orders, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "read_trades",
        )

        self._check_root(root)

        book = "read_trades"

        agent = TradingAgent(root, new_user=True)

        for order in orders:
            agent.new_record(book, order, new_book=True)

        books = agent.books()
        self.assertEqual(len(books), 1)

        trades = agent.read_trades(book)

        self.assertEqual(len(trades), expected["length"])

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 3},
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 6},
            },
        ]
    )
    def test_read_records(self, orders, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "read_records",
        )

        self._check_root(root)

        book = "read_records"

        agent = TradingAgent(root, new_user=True)

        for order in orders:
            agent.new_record(book, order, new_book=True)

        books = agent.books()
        self.assertEqual(len(books), 1)

        records = agent.read_records(book)

        self.assertEqual(len(records), expected["length"])

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders_a": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "orders_b": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
            {
                "orders_a": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "orders_b": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 8},
            },
            {
                "orders_a": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "orders_b": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
            {
                "orders_a": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "orders_b": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
        ]
    )
    def test_read_all_records(self, orders_a, orders_b, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "read_all_records",
        )

        self._check_root(root)

        book_a = "read_all_records_a"
        book_b = "read_all_records_b"

        agent = TradingAgent(root, new_user=True)

        for order in orders_a:
            agent.new_record(book_a, order, new_book=True)

        for order in orders_b:
            agent.new_record(book_b, order, new_book=True)

        books = agent.books()
        self.assertEqual(len(books), 2)

        records = agent.read_all_records()
        self.assertEqual(len(records), expected["length"])

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
            {
                "orders": [
                    {
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 3},
            },
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 6},
            },
        ]
    )
    def test_new_order(self, orders, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "orders",
        )

        self._check_root(root)

        agent = TradingAgent(root, new_user=True)
        agent.delete_all_orders()

        for order in orders:
            agent.new_order(order)

        orders = agent.read_orders()

        self.assertEqual(len(orders), expected["length"])

        for i in range(len(orders)):
            agent.delete_order(0)
            orders = agent.read_orders()
            self.assertEqual(len(orders), expected["length"] - (i + 1))

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders": [
                    {
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                    {
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
                "events": [{"dtime": "20191231", "price": 110}],
                "expected": [
                    {
                        "datetime": "20191231",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
            },
            {
                "orders": [
                    {
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "120",
                    },
                    {
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                    {
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
                "events": [
                    {"dtime": "20191229", "price": 110},
                    {"dtime": "20191231", "price": 90},
                ],
                "expected": [
                    {
                        "datetime": "20191229",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                    {
                        "datetime": "20191231",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
            },
        ]
    )
    def test_check_orders(self, orders, events, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "check_orders",
        )

        self._check_root(root)

        book = "check_orders"

        agent = TradingAgent(root, new_user=True)
        agent.delete_all_orders()

        for order in orders:
            agent.new_order(order)

        self.assertEqual(len(orders), len(agent.read_orders()))

        self.assertEqual(len(events), len(expected))

        for ei, event in enumerate(events):
            agent.check_orders(
                book,
                datetime.strptime(event["dtime"], "%Y%m%d"),
                event["price"],
                new_book=True,
            )

            self.assertEqual(len(orders) - (ei + 1), len(agent.read_orders()))

            ts = agent.read_records(book)

            self.assertTrue(ts is not None)
            self.assertNotEqual(len(ts), 0)

            for i, t in enumerate(ts):
                te = t.to_entity()
                ee = expected[i]

                self.assertEqual(te["datetime"], ee["datetime"])
                self.assertEqual(te["symbol"], ee["symbol"])
                self.assertEqual(te["operation"], ee["operation"])
                self.assertEqual(float(te["leverage"]), float(ee["leverage"]))
                self.assertEqual(float(te["price"]), float(ee["price"]))

        self._clean_root(root)


if __name__ == "__main__":
    unittest.main()
