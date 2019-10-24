import time
import unittest
from datetime import datetime

from fun.trading.book import TradingBook
from fun.utils import helper


class TestBook(unittest.TestCase):

    dtime = datetime.strptime("2019-03-13", "%Y-%m-%d")

    def test_init_succeed(self):

        trading_book = TradingBook(
            dtime=self.dtime, symbol="esz19", version="1", note="hello", book_type="PAPER"
        )

        self.assertEqual(trading_book.time, self.dtime)
        self.assertEqual(trading_book.symbol, "esz19")
        self.assertEqual(trading_book.version, "1")
        self.assertEqual(trading_book.note, "hello")
        self.assertEqual(trading_book.book_type, "paper")

        self.assertNotEqual(trading_book.last_modified, 0)
        self.assertNotEqual(trading_book.index, "")

        last_time = time.time()
        last_index = helper.random_string(length=16)

        trading_book = TradingBook(
            dtime=self.dtime,
            symbol="spx",
            version="1",
            note="HELLO",
            book_type="LIVE",
            last_modified=last_time,
            index=last_index,
        )

        self.assertEqual(trading_book.time, self.dtime)
        self.assertEqual(trading_book.symbol, "spx")
        self.assertEqual(trading_book.version, "1")
        self.assertEqual(trading_book.note, "HELLO")
        self.assertEqual(trading_book.book_type, "live")
        self.assertEqual(trading_book.last_modified, last_time)
        self.assertEqual(trading_book.index, last_index)

    def test_init_invalid(self):

        tables = [
            {
                "inputs": {
                    "dtime": -1,
                    "symbol": "rut",
                    "version": "1",
                    "note": "hello",
                    "book_type": "paper",
                }
            },
            {
                "inputs": {
                    "dtime": self.dtime,
                    "symbol": "qrz19",
                    "version": "1",
                    "note": "hello",
                    "book_type": "WORLD",
                }
            },
            {
                "inputs": {
                    "dtime": self.dtime,
                    "symbol": "tyz19",
                    "version": "1",
                    "note": "hello",
                    "book_type": "PAPER",
                    "index": "[]",
                }
            },
            {
                "inputs": {
                    "dtime": self.dtime,
                    "symbol": "19",
                    "version": "1",
                    "note": "hello",
                    "book_type": "PAPER",
                }
            },
            {
                "inputs": {
                    "dtime": self.dtime,
                    "symbol": "esa19",
                    "version": "1",
                    "note": "hello",
                    "book_type": "PAPER",
                }
            },
            {
                "inputs": {
                    "dtime": self.dtime,
                    "symbol": "esz19",
                    "version": "",
                    "note": "hello",
                    "book_type": "live",
                }
            },
        ]

        for table in tables:
            with self.assertRaises(ValueError):
                TradingBook(
                    dtime=table["inputs"]["dtime"],
                    symbol=table["inputs"]["symbol"],
                    version=table["inputs"]["version"],
                    note=table["inputs"]["note"],
                    book_type=table["inputs"]["book_type"],
                    index=table["inputs"].get("index", ""),
                )

    def test_has_modified_succeed(self):
        trading_book = TradingBook(
            dtime=self.dtime, symbol="spx", version="1", note="hello", book_type="PAPER"
        )
        last_modified = trading_book.last_modified
        trading_book.has_modified()

        self.assertNotEqual(last_modified, trading_book.last_modified)
        self.assertLess(last_modified, trading_book.last_modified)

    def test_entity_succeed(self):
        trading_book = TradingBook(
            dtime=self.dtime, symbol="spx", version="1", note="hello", book_type="PAPER"
        )

        self.assertEqual(trading_book.to_entity().get("time", ""), "20190313")
        self.assertEqual(trading_book.to_entity().get("symbol", ""), "spx")
        self.assertEqual(trading_book.to_entity().get("version", ""), "1")
        self.assertEqual(trading_book.to_entity().get("note", ""), "hello")
        self.assertEqual(trading_book.to_entity().get("book_type", ""), "paper")

        self.assertEqual(
            trading_book.to_entity().get("last_modified", ""),
            str(trading_book.last_modified),
        )

        self.assertEqual(trading_book.to_entity().get("index", ""), trading_book.index)

    def test_entity_exchange_succeed(self):
        trading_book = TradingBook(
            dtime=self.dtime, symbol="nqz19", version="1", note="hello", book_type="PAPER"
        )
        new_book = TradingBook.from_entity(trading_book.to_entity())

        self.assertEqual(trading_book.index, new_book.index)
        self.assertEqual(trading_book.last_modified, new_book.last_modified)
        self.assertEqual(trading_book.time, new_book.time)
        self.assertEqual(trading_book.symbol, new_book.symbol)
        self.assertEqual(trading_book.version, new_book.version)
        self.assertEqual(trading_book.note, new_book.note)
        self.assertEqual(trading_book.book_type, new_book.book_type)

    def test_trading_book_from_entity_succeed(self):
        entity = {
            "time": "20190313",
            "symbol": "compq",
            "version": "1",
            "note": "hello world",
            "book_type": "paper",
        }

        trading_book = TradingBook.from_entity(entity)

        self.assertEqual(
            trading_book.time.strftime("%Y-%m-%d"), self.dtime.strftime("%Y-%m-%d")
        )

        self.assertEqual(trading_book.symbol, "compq")
        self.assertEqual(trading_book.version, "1")

        self.assertEqual(trading_book.note, "hello world")
        self.assertEqual(trading_book.book_type, "paper")

        self.assertNotEqual(trading_book.last_modified, 0)
        self.assertNotEqual(trading_book.index, "")

    def test_trading_book_from_entity_missing_necessary_key(self):

        entities = [
            {
                "note": "hello world",
                "symbol": "spx",
                "version": "1",
                "book_type": "paper",
            },
            {
                "time": "20190313",
                "symbol": "spx",
                "version": "1",
                "note": "hello world",
            },
            {
                "time": "20190313",
                "book_type": "paper",
                "version": "1",
                "note": "hello world",
            },
            {
                "time": "20190313",
                "book_type": "paper",
                "symbol": "rut",
                "note": "hello world",
            },
        ]

        for entity in entities:
            with self.assertRaises(KeyError):
                TradingBook.from_entity(entity)
