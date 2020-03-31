import os
import unittest
from typing import cast

from fun.utils.jsondb import JsonDB
from fun.utils.testing import parameterized


class TestJsonDB(unittest.TestCase):

    test_root = os.path.join(
        cast(str, os.getenv("HOME")), "Documents", "database", "json", "testing"
    )

    def _check_database(self, database, db, col, entities, queries, expected):
        for i, q in enumerate(queries):
            results = database.find(db, col, q)
            e = expected[i]

            if results is None:
                self.assertEqual(len(e), 0)
                continue

            self.assertEqual(len(results), len(expected[i]))

            if len(e) == 0:
                self.assertIsNone(results)
            else:
                for j, r in enumerate(results):
                    for k in r.keys():
                        rk = r.get(k, None)
                        ek = e[j].get(k, None)
                        if rk is None:
                            self.assertIsNone(ek)
                        else:
                            self.assertEqual(rk, ek)

        for entity in entities:
            database.delete(db, col, entity)
            result = database.find(db, col, entity)
            self.assertIsNone(result)

    def setUp(self):
        self.assertTrue(os.path.exists(self.test_root))

    @parameterized(
        [
            {
                "entities": [
                    ##
                    {"a": "1", "b": "2"},
                ],
                "queries": [
                    ##
                    {"a": "1"},
                    {"b": "2"},
                    {"c": "3"},
                    {"a": "1", "b": "2"},
                    {"a": "1", "b": "2", "c": "3"},
                ],
                "expected": [
                    ##
                    [
                        ##
                        {"a": "1", "b": "2"},
                    ],
                    [
                        ##
                        {"a": "1", "b": "2"},
                    ],
                    [
                        ##
                    ],
                    [
                        ##
                        {"a": "1", "b": "2"},
                    ],
                    [
                        ##
                    ],
                ],
                "new_entities": [],
                "new_queries": [],
                "new_expected": [
                    ##
                    [],
                ],
            },
            {
                "entities": [
                    ##
                    {"s": "0", "a": "1", "b": "2"},
                    {"s": "0", "c": "3", "d": "4"},
                ],
                "queries": [
                    ##
                    {"s": "0"},
                    {"a": "1"},
                    {"b": "2"},
                    {"c": "3"},
                    {"d": "4"},
                    {"e": "7"},
                    {"c": "3", "d": "4"},
                    {"s": "0", "d": "4"},
                    {"s": "0", "b": "2"},
                    {"s": "0", "a": "1", "b": "2"},
                    {"s": "0", "c": "3", "d": "4"},
                ],
                "expected": [
                    ##
                    [
                        ##
                        {"s": "0", "a": "1", "b": "2"},
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                        {"s": "0", "a": "1", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "0", "a": "1", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                    ],
                    [
                        ##
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                        {"s": "0", "a": "1", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "0", "a": "1", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                ],
                "new_entities": [],
                "new_queries": [],
                "new_expected": [
                    ##
                    [],
                ],
            },
            {
                "entities": [
                    ##
                    {"s": "0", "a": "1", "b": "2"},
                    {"s": "0", "c": "3", "d": "4"},
                    {"hello": "world"},
                ],
                "queries": [
                    ##
                    {"s": "0"},
                    {"a": "1"},
                    {"c": "3"},
                    {"c": "3", "d": "4"},
                    {"e": "7"},
                ],
                "expected": [
                    ##
                    [
                        ##
                        {"s": "0", "a": "1", "b": "2"},
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                        {"s": "0", "a": "1", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                        {"s": "0", "c": "3", "d": "4"},
                    ],
                    [
                        ##
                    ],
                ],
                "new_entities": [
                    ##
                    {"s": "0", "a": "10", "b": "2"},
                    {"s": "5", "c": "3", "d": "4", "b": "2"},
                    {"hello": "world"},
                ],
                "new_queries": [
                    ##
                    {"s": "0"},
                    {"s": "5"},
                    {"a": "1"},
                    {"a": "10"},
                    {"b": "2"},
                    {"c": "3"},
                    {"c": "3", "d": "4"},
                    {"hello": "world"},
                ],
                "new_expected": [
                    ##
                    [
                        ##
                        {"s": "0", "a": "10", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "5", "c": "3", "d": "4", "b": "2"},
                    ],
                    [
                        ##
                    ],
                    [
                        ##
                        {"s": "0", "a": "10", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "0", "a": "10", "b": "2"},
                        {"s": "5", "c": "3", "d": "4", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "5", "c": "3", "d": "4", "b": "2"},
                    ],
                    [
                        ##
                        {"s": "5", "c": "3", "d": "4", "b": "2"},
                    ],
                    [
                        ##
                        {"hello": "world"},
                    ],
                ],
            },
        ]
    )
    def test_db(
        self, entities, queries, expected, new_entities, new_queries, new_expected
    ):
        db = "test"
        col = "test"

        database = JsonDB(database_root=self.test_root)

        if os.path.exists(os.path.join(self.test_root, f"{db}_{col}.json")):
            database.drop(db, col)
            self.assertFalse(
                os.path.exists(os.path.join(self.test_root, f"{db}_{col}.json"))
            )

        database.insert(db, col, *entities)

        self._check_database(database, db, col, entities, queries, expected)

        if len(new_entities) != 0 and len(new_queries) != 0:
            self.assertEqual(len(entities), len(new_entities))

            database.insert(db, col, *entities)

            for i, e in enumerate(entities):
                database.replace(db, col, e, new_entities[i])

            self._check_database(
                database, db, col, new_entities, new_queries, new_expected
            )

        database.drop(db, col)
        self.assertFalse(
            os.path.exists(os.path.join(self.test_root, f"{db}_{col}.json"))
        )


if __name__ == "__main__":
    unittest.main()
