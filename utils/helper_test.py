import unittest

from fun.utils import helper


class TestHelper(unittest.TestCase):
    def test_random_string(self):
        for _ in range(1000):
            rand_string_01 = helper.random_string()
            rand_string_02 = helper.random_string()

            self.assertNotEqual(rand_string_01, rand_string_02)

    def test_key_value_pair_succeed(self):
        inputs = "price=100;op=l"
        pair = helper.key_value_pair(inputs)

        tables = [
            {"inputs": "price=100;op=l", "expected": {"price": "100", "op": "l"}},
            {"inputs": "price=100 ; op=l", "expected": {"price": "100", "op": "l"}},
            {
                "inputs": "price=100.5 ; note=hello world",
                "expected": {"price": "100.5", "note": "hello world"},
            },
            {"inputs": "action=+ ; op=-", "expected": {"action": "+", "op": "-"}},
        ]

        for table in tables:
            pair = helper.key_value_pair(table["inputs"])

            for k, v in table["expected"].items():
                self.assertEqual(pair.get(k, None), v)

    def test_key_value_pair_empty(self):

        tables = [{"inputs": ""}, {"inputs": "price=;o=l"}, {"inputs": "=100.5;o=l"}]

        for table in tables:
            with self.assertRaises(ValueError):
                helper.key_value_pair(table["inputs"])
