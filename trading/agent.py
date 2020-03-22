import os
from typing import List, Optional

from fun.trading.book import TradingBook
from fun.trading.transaction import FuturesTransaction
from fun.utils.jsondb import JsonDB


class Agent:

    _DB_ADMIN = "admin"
    _DB_TRADING_BOOK = "trading_books"
    _DB_TRADING_RECORDS = "succeed"

    _COL_USER = "user"

    def __init__(self, user_name: str) -> None:
        home = os.getenv("HOME")
        assert home is not None

        path = os.path.join(home, "Documents/database/market_wizards")
        assert os.path.exists(path)

        self._db = JsonDB(path)

        self._uid = self._login(user_name)

    def _login(self, user_name: str) -> str:
        users = self._db.find(
            database=self._DB_ADMIN,
            collection=self._COL_USER,
            query={"name": user_name},
        )

        if users is not None and len(users) == 1:
            uid = users[0].get("uid", None)
            assert uid is not None
            return uid
        else:
            raise ValueError("invalid user name")

    def books(self) -> Optional[List[TradingBook]]:
        books = self._db.find(
            database=self._DB_TRADING_BOOK, collection=self._uid, query=None
        )

        if books is not None and len(books) > 0:
            bs = [TradingBook.from_entity(b) for b in books]
            bs.sort(key=lambda b: b.last_modified())
            return bs
        else:
            return None

    def read_records(self, title: str) -> Optional[List[FuturesTransaction]]:
        assert title != ""

        books = self.books()
        if books is None or len(books) == 0:
            return None

        books.sort(key=lambda b: b.last_modified())

        for b in books:
            if b.title() == title:
                entities = self._db.find(
                    f"{self._DB_TRADING_RECORDS}", b.index(), query=None
                )
                if entities is None or len(entities) == 0:
                    continue
                else:
                    return [FuturesTransaction.from_entity(e) for e in entities]

        return None

    def read_all_records(self) -> Optional[List[FuturesTransaction]]:

        books = self.books()
        if books is None or len(books) == 0:
            return None

        books.sort(key=lambda b: b.last_modified())

        ts: List[FuturesTransaction] = []
        for b in books:
            entities = self._db.find(
                f"{self._DB_TRADING_RECORDS}", b.index(), query=None
            )
            if entities is None or len(entities) == 0:
                continue

                ts.extend([FuturesTransaction.from_entity(e) for e in entities])

        return ts
