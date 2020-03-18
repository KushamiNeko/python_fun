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

    def __init__(self, user_name: str) -> None:
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
            bs = [TradingBook.from_entity(b) for b in books]
            bs.sort(key=lambda b: b.time.year)
            return bs
        else:
            return None

    def read_records(
        self, symbol: str, year: int, version: str
    ) -> Optional[List[FuturesTransaction]]:
        assert symbol != ""

        books = self.books()
        if books is None or len(books) == 0:
            return None

        for b in books:
            if b.symbol == symbol and b.time.year == year and b.version == version:
                entities = self._db.find(f"{b.book_type}_trading", b.index, query=None)
                if entities is None or len(entities) == 0:
                    continue
                else:
                    return [FuturesTransaction.from_entity(e) for e in entities]

        return None

    def read_all_records(
        self, symbol: str, version: str
    ) -> Optional[List[FuturesTransaction]]:

        assert symbol != ""

        books = self.books()
        if books is None or len(books) == 0:
            return None

        ts = []
        for b in books:
            if b.symbol == symbol and b.version == version:
                entities = self._db.find(f"{b.book_type}_trading", b.index, query=None)
                if entities is None or len(entities) == 0:
                    continue

                ts.extend([FuturesTransaction.from_entity(e) for e in entities])

        return ts
