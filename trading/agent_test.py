import os
import unittest
from typing import Dict, List, cast

from fun.trading.agent import TradingAgent
from fun.utils.jsondb import JsonDB
from fun.utils.testing import parameterized


class TestTradingAgent(unittest.TestCase):

    _root = os.path.join(
        cast(str, os.getenv("HOME")), "Documents", "database", "testing", "json"
    )

    def setUp(self):
        self.assertTrue(os.path.exists(self._root))

    def _check_database(
        self, db: str, col: str, expected: List[Dict[str, str]], remove_db=True
    ):
        self.assertTrue(os.path.exists(os.path.join(self._root, f"{db}_{col}.json")))

        jsonDB = JsonDB(self._root)
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

        if remove_db:
            jsonDB.drop(db, col)

    @parameterized(
        [
            {"user_name": "new", "new_user": True, "error": None,},
            {"user_name": "nonexist", "new_user": False, "error": ValueError,},
        ]
    )
    def test_init(self, user_name, new_user, error):
        if error is not None:
            with self.assertRaises(ValueError):
                TradingAgent(
                    self._root, user_name=user_name, new_user=new_user,
                )
        else:
            TradingAgent(
                self._root, user_name=user_name, new_user=new_user,
            )

            self._check_database("admin", "user", [{"name": "new", "uid": ""}])

    def test_new_order(self):
        pass

    def test_check_orders(self):
        pass

    def test_read_records(self):
        pass

    def test_read_all_records(self):
        pass
