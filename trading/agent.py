import os
from typing import List, Optional

from fun.trading.book import TradingBook
from fun.trading.transaction import FuturesTransaction
from fun.utils.jsondb import JsonDB


class Agent:

    _DB_ADMIN = "admin"
    _DB_TRADING_BOOK = "trading_books"
    _DB_PAPER_TRADING = "paper_trading"
    _DB_LIVE_TRADING = "live_trading"

    _COL_USER = "user"

    def __init__(self, user_name: str):
        home = os.getenv("HOME")
        assert home is not None

        self._db = JsonDB(os.path.join(home, "Documents/database/json/market_wizards"))

        self._uid = self._login(user_name)

    def _login(self, user_name: str) -> str:
        users = self._db.find(
            database=self._DB_ADMIN,
            collection=self._COL_USER,
            query={"name": user_name},
        )

        if users is not None and len(users) == 1:
            uid = users[0].get("uid", "")
            assert uid is not None
            return uid
        else:
            raise ValueError("invalid user name")

    def books(self) -> Optional[List[TradingBook]]:
        books = self._db.find(
            database=self._DB_TRADING_BOOK, collection=self._uid, query=None
        )

        if books is not None:
            return [TradingBook.from_entity(b) for b in books]
        else:
            return books

    def read_records(
        self, symbol: str, year: int, version: int
    ) -> Optional[List[FuturesTransaction]]:
        assert symbol != ""

        books = self.books()
        if books is None or len(books) == 0:
            return None

        index: Optional[str] = None
        book_type: Optional[str] = None
        for b in books:
            if b.symbol == symbol and b.time.year == year and b.version == version:
                index = b.index
                book_type = b.book_type

        if index is None or book_type is None:
            return None

        entities = self._db.find(f"{book_type}_trading", index, query=None)

        if entities is None or len(entities) == 0:
            return None

        return [FuturesTransaction.from_entity(e) for e in entities]
