import os
import unittest

from fun.utils.jsondb import JsonDB


class TestJsonDB(unittest.TestCase):

    database = None
    test_root = ""
    test_database = "test"
    test_collection = "test"

    @classmethod
    def setUpClass(cls):
        assert os.getenv("HOME")

        cls.test_root = os.path.join(
            os.getenv("HOME"), "Documents", "database", "json", "testing"
        )

        assert os.path.exists(cls.test_root)

        cls.database = JsonDB(database_root=cls.test_root)

    @classmethod
    def tearDownClass(cls):
        cls.database.drop_collection(cls.test_database, cls.test_collection)

        assert not os.path.exists(
            os.path.join(
                cls.test_root, f"{cls.test_database}_{cls.test_collection}.json"
            )
        )

    def setUp(self):
        self.assertIsNotNone(self.database)
        self.assertTrue(os.path.exists(self.test_root))

    def test_insert_find_delete_succeed(self):
        entity = {"a": "1", "b": "2"}

        self.database.insert(self.test_database, self.test_collection, entity)

        result = self.database.find(self.test_database, self.test_collection, entity)

        self.assertEqual(len(result), 1)

        self.assertEqual(result[0]["a"], entity["a"])
        self.assertEqual(result[0]["b"], entity["b"])

        self.database.delete(self.test_database, self.test_collection, entity)

        result = self.database.find(self.test_database, self.test_collection, entity)

        self.assertIsNone(result)

    def test_insert_find_delete_multiple_succeed(self):
        entity_1 = {"s": "0", "a": "1", "b": "2"}

        entity_2 = {"s": "0", "c": "3", "d": "4"}

        query = {"s": "0"}

        self.database.insert(
            self.test_database, self.test_collection, entity_1, entity_2
        )

        results = self.database.find(self.test_database, self.test_collection, query)

        self.assertEqual(len(results), 2)

        for result in results:
            if "a" in result:

                self.assertEqual(result["s"], entity_1["s"])
                self.assertEqual(result["a"], entity_1["a"])
                self.assertEqual(result["b"], entity_1["b"])

            if "c" in result:

                self.assertEqual(result["s"], entity_2["s"])
                self.assertEqual(result["c"], entity_2["c"])
                self.assertEqual(result["d"], entity_2["d"])

        self.database.delete(self.test_database, self.test_collection, query)
        results = self.database.find(self.test_database, self.test_collection, query)

        self.assertEqual(len(results), 1)

        self.database.delete(self.test_database, self.test_collection, query)
        results = self.database.find(self.test_database, self.test_collection, query)

        self.assertIsNone(results)

    def test_replace_succeed(self):
        entity = {"a": "1", "b": "2"}

        new_entity = {"a": "0", "b": "2"}

        query = {"b": "2"}

        self.database.insert(self.test_database, self.test_collection, entity)

        self.database.replace(
            self.test_database, self.test_collection, query, new_entity
        )

        result = self.database.find(self.test_database, self.test_collection, query)

        self.assertIsNotNone(result)

        self.assertEqual(len(result), 1)

        self.assertEqual(result[0]["a"], new_entity["a"])
        self.assertEqual(result[0]["b"], new_entity["b"])

        self.database.delete(self.test_database, self.test_collection, query)

        result = self.database.find(self.test_database, self.test_collection, entity)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
