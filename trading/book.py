from __future__ import annotations

import re
import time
from datetime import datetime
from typing import Dict, Optional

from fun.utils import helper


class TradingBook:
    def __init__(
        self,
        dtime: datetime,
        symbol: str,
        version: str,
        note: str,
        book_type: str,
        index: Optional[str] = None,
        last_modified: Optional[float] = None,
    ):

        self._note = note.strip()

        if type(dtime) != datetime:
            raise ValueError("invalid book time")
        self._time = dtime

        if not re.match(r"^(?:paper|live)$", book_type.lower()):
            raise ValueError("invalid book type")
        self._book_type = book_type.lower()

        if not re.match(r"^[a-z]+(?:[fghjkmnquvxz][0-9]+)?$", symbol.lower()):
            raise ValueError("invalid book symbol")
        self._symbol = symbol.lower()

        if version == "":
            raise ValueError("invalid book version")
        self._version = version

        if last_modified is None or last_modified <= 0:
            self._last_modified = time.time()
        else:
            self._last_modified = last_modified

        if index is None or index == "":
            self._index = helper.random_string(length=16)
        else:
            if not re.match(r"^[0-9a-zA-Z]+$", index):
                raise ValueError("invalid book index")
            self._index = index

    @property
    def index(self) -> str:
        return self._index

    @property
    def time(self) -> datetime:
        return self._time

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def version(self) -> str:
        return self._version

    @property
    def book_type(self) -> str:
        return self._book_type

    @property
    def last_modified(self) -> float:
        return self._last_modified

    @property
    def note(self) -> str:
        return self._note

    def has_modified(self) -> None:
        self._last_modified = time.time()

    def to_entity(self) -> Dict[str, str]:
        return {
            "index": self._index,
            "time": self._time.strftime("%Y%m%d"),
            "symbol": self._symbol,
            "version": str(self._version),
            "book_type": self._book_type,
            "last_modified": str(self._last_modified),
            "note": self._note,
        }

    @classmethod
    def from_entity(cls, entity: Dict[str, str]) -> TradingBook:

        return cls(
            book_type=entity["book_type"],
            dtime=datetime.strptime(entity["time"], "%Y%m%d"),
            symbol=entity["symbol"],
            version=entity["version"],
            note=entity.get("note", ""),
            last_modified=float(entity.get("last_modified", "0")),
            index=entity.get("index", ""),
        )
