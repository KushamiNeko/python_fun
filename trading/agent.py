import os
from datetime import datetime
from typing import Dict, List, Optional

from fun.trading.book import TradingBook
from fun.trading.order import TransactionOrder
from fun.trading.transaction import FuturesTransaction
from fun.utils.helper import random_string
from fun.utils.jsondb import JsonDB


class Agent:

    _DB_ADMIN = "admin"

    _DB_TRADING_BOOKS = "books"
    _DB_TRADING_RECORDS = "records"
    _DB_TRADING_ORDERS = "orders"

    _COL_USER = "user"

    _ORDERS: List[TransactionOrder] = []

    @classmethod
    def _new_order(cls, entiry: Dict[str, str]) -> None:
        o = TransactionOrder.from_entity(entiry)
        cls._ORDERS.append(o)

    @classmethod
    def _check_order(cls, stop_price: float) -> Optional[List[TransactionOrder]]:
        orders = []

        for order in cls._ORDERS:
            if order.operation() == "+":
                if order.price() >= stop_price:
                    orders.append(order)
            elif order.operation() == "-":
                if order.price() <= stop_price:
                    orders.append(order)

        if len(orders) == 0:
            return None
        else:
            return orders

    def __init__(
        self, root: str = "", user_name: str = "default", new_user: bool = False
    ) -> None:
        home = os.getenv("HOME")
        assert home is not None

        if root == "":
            root = os.path.join(home, "Documents/database/market_wizards")

        assert os.path.exists(root)

        self._db = JsonDB(root)

        self._uid = self._login(user_name, new_user)

    def _login(self, user_name: str, new_user: bool) -> str:
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
            if new_user:
                uid = random_string()

                self._db.insert(
                    self._DB_ADMIN, self._COL_USER, {"name": user_name, "uid": uid},
                )

                return uid
            else:
                raise ValueError("invalid user name")

    def _find_book(self, title: str) -> Optional[TradingBook]:
        books = self.books()
        if books is not None:
            for b in books:
                if b.title() == title:
                    return b

        return None

    def books(self) -> Optional[List[TradingBook]]:
        books = self._db.find(
            database=self._DB_TRADING_BOOKS, collection=self._uid, query=None
        )

        if books is not None and len(books) > 0:
            bs = [TradingBook.from_entity(b) for b in books]
            bs.sort(key=lambda b: b.last_modified())
            return bs
        else:
            return None

    def new_record(
        self, title: str, entity: Dict[str, str], new_book: bool = False
    ) -> FuturesTransaction:
        assert title != ""

        book = self._find_book(title)
        if book is None:
            if new_book:
                book = TradingBook(title=title)
                self._db.insert(
                    self._DB_TRADING_BOOKS, self._uid, book.to_entity(),
                )
            else:
                raise ValueError(f"book {title} does not exist")

        t = FuturesTransaction.from_entity(entity)
        self._db.insert(self._DB_TRADING_RECORDS, book.index(), t.to_entity())

        return t

    def new_order(self, entity: Dict[str, str]) -> None:
        self._new_order(entity)

    def check_orders(self, title: str, dtime: datetime, stop_price: float) -> None:
        orders = self._check_order(stop_price)
        if orders is None:
            return
        else:
            for order in orders:
                entity = order.to_entity()
                entity["datetime"] = dtime.strftime("%Y%m%b")

                self.new_record(title, entity)

    def read_records(self, title: str) -> Optional[List[FuturesTransaction]]:
        assert title != ""

        book = self._find_book(title)
        if book is not None:
            entities = self._db.find(self._DB_TRADING_RECORDS, book.index(), query=None)
            if entities is not None and len(entities) != 0:
                return [FuturesTransaction.from_entity(e) for e in entities]

        return None

    def read_all_records(self) -> Optional[List[FuturesTransaction]]:

        books = self.books()
        if books is None or len(books) == 0:
            return None

        ts: List[FuturesTransaction] = []
        for b in books:
            entities = self._db.find(
                f"{self._DB_TRADING_RECORDS}", b.index(), query=None
            )
            if entities is None or len(entities) == 0:
                continue

                ts.extend([FuturesTransaction.from_entity(e) for e in entities])

        return ts
