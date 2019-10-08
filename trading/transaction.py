from __future__ import annotations

import re
import time
from datetime import datetime
from typing import Dict, Optional

from fun.utils import helper


class FuturesTransaction:
    def __init__(
        self,
        dtime: datetime,
        symbol: str,
        operation: str,
        quantity: int,
        price: float,
        note: str,
        index: Optional[str] = None,
        time_stamp: Optional[float] = None,
    ):

        if index is None or index == "":
            self._index = helper.random_string(length=16)
        else:
            if not re.match(r"[0-9a-zA-Z]+", index):
                raise ValueError("invalid transaction index")
            self._index = index

        if time_stamp is None or time_stamp <= 0:
            self._time_stamp = time.time()
        else:
            self._time_stamp = time_stamp

        if type(dtime) != datetime:
            raise ValueError("invalid transaction time")
        self._time = dtime

        if not re.match(r"^[a-zA-Z]+$", symbol):
            raise ValueError("invalid transaction symbol")
        self._symbol = symbol.lower()

        if not re.match(r"^(?:long|short|increase|decrease|close)$", operation.lower()):
            raise ValueError("invalid transaction operation")
        self._operation = operation.lower()

        if quantity <= 0 or type(quantity) != int:
            raise ValueError("invalid transaction quantity")
        self._quantity = quantity

        if price <= 0.0:
            raise ValueError("invalid transaction price")
        self._price = price

        self._note = note.strip()

    @property
    def index(self) -> str:
        return self._index

    @property
    def time_stamp(self) -> float:
        return self._time_stamp

    @property
    def time(self) -> datetime:
        return self._time

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def operation(self) -> str:
        return self._operation

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def price(self) -> float:
        return self._price

    @property
    def note(self) -> str:
        return self._note

    @property
    def total_cost(self) -> float:
        return self._price * self._quantity

    def to_entity(self) -> Dict[str, str]:
        return {
            "index": self._index,
            "time_stamp": str(self._time_stamp),
            "time": self._time.strftime("%Y-%m-%d"),
            "symbol": self._symbol,
            "operation": self._operation,
            "quantity": str(self._quantity),
            "price": str(self._price),
            "note": self._note,
        }

    @classmethod
    def from_entity(cls, entity: Dict[str, str]) -> FuturesTransaction:
        return cls(
            dtime=datetime.strptime(entity["time"], "%Y-%m-%d"),
            symbol=entity["symbol"],
            operation=entity["operation"],
            quantity=int(entity["quantity"]),
            price=float(entity["price"]),
            note=entity.get("note", ""),
            index=entity.get("index", ""),
            time_stamp=float(entity.get("time_stamp", 0)),
        )
