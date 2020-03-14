from __future__ import annotations

import re
from datetime import datetime
from typing import Optional, List

import pandas as pd

from fun.data import continuous

ALL_CONTRACT_MONTHS = "fghjkmnquvxz"
EVEN_CONTRACT_MONTHS = "gjmqvz"
FINANCIAL_CONTRACT_MONTHS = "hmuz"


class Contract:

    _barchart_format = r"(\w{2})([fghjkmnquvxz])(\d{2})"
    _quandl_format = r"([\d\w]+)([fghjkmnquvxz])(\d{4})"

    @classmethod
    def front_month(
        cls,
        symbol: str,
        months: str,
        fmt: str,
        read_data: bool = True,
        time: datetime = datetime.now(),
    ) -> Contract:
        assert fmt in ("barchart", "quandl")
        assert months in (
            ALL_CONTRACT_MONTHS,
            EVEN_CONTRACT_MONTHS,
            FINANCIAL_CONTRACT_MONTHS,
        )

        front_year = time.year

        front_month = ""
        if months == FINANCIAL_CONTRACT_MONTHS:
            offset = time.month + 1
            if offset > 12:
                offset %= 13
                front_year += 1

            for m in months:
                if month_from_futures_month_code(m) > time.month:
                    front_month = m
                    break
        else:
            offset = time.month + 2
            if offset > 12:
                offset %= 13
                front_year += 1

            for m in months:
                if month_from_futures_month_code(m) > offset:
                    front_month = m
                    break

        if fmt == "barchart":
            front_year %= 100

        return Contract(
            code=f"{symbol}{front_month}", fmt=fmt, months=months, read_data=read_data
        )

    def __init__(
        self,
        code: str,
        months: str,
        fmt: str,
        read_data: bool = True,
        df: Optional[pd.DataFrame] = None,
    ) -> None:

        assert fmt in ("barchart", "quandl")
        assert months in (
            ALL_CONTRACT_MONTHS,
            EVEN_CONTRACT_MONTHS,
            FINANCIAL_CONTRACT_MONTHS,
        )

        self._df = df
        if read_data:
            self.read_data()

        self._code = code
        self._fmt = fmt
        self._months = months

        symbol = ""
        year = 0
        month = 0

        match = None

        if self._fmt == "barchart":
            match = re.match(self._barchart_format, self._code)
            if match is None:
                raise ValueError(
                    f"invalid contract code {self._code} for {self._fmt} format"
                )

            year = int(f"20{match.group(3)}")

        elif self._fmt == "quandl":
            match = re.match(self._quandl_format, self._code)
            if match is None:
                raise ValueError(
                    f"invalid contract code {self._code} for {self._fmt} format"
                )

            year = int(match.group(3))

        else:
            raise ValueError("unknown contract code format: {self._fmt}")

        assert match is not None

        symbol = match.group(1)
        month = month_from_futures_month_code(match.group(2))

        assert symbol != ""
        assert year != 0
        assert month != 0

        if year > datetime.now().year:
            year -= 100

        self._symbol = symbol
        self._year = year
        self._month = month

    def read_data(self) -> None:
        src = continuous.Contract()
        self._df = src.read(datetime(1776, 7, 4), datetime.now(), self._code, "d")
        assert self._df is not None

    def code(self) -> str:
        return self._code

    def symbol(self) -> str:
        return self._symbol

    def year(self) -> int:
        return self._year

    def month(self) -> int:
        return self._month

    # def previous_contract(self) -> str:
    def previous_contract(self, read_data: bool = True) -> Contract:
        p_year = self.year()
        mi = self._months.index(month_to_futures_month_code(self._month))
        if mi - 1 < 0:
            p_year -= 1

        p_month = month_from_futures_month_code(
            self._months[mi - 1 % len(self._months)]
        )

        if self._fmt == "barchart":
            p_year %= 100

        # return f"{self._symbol}{month_to_futures_month_code(p_month)}{p_year}"

        return Contract(
            code=f"{self._symbol}{month_to_futures_month_code(p_month)}{p_year}",
            months=self._months,
            fmt=self._fmt,
            read_data=read_data,
        )


def month_to_futures_month_code(month: int) -> str:
    if month == 1:
        return "f"
    elif month == 2:
        return "g"
    elif month == 3:
        return "h"
    elif month == 4:
        return "j"
    elif month == 5:
        return "k"
    elif month == 6:
        return "m"
    elif month == 7:
        return "n"
    elif month == 8:
        return "q"
    elif month == 9:
        return "u"
    elif month == 10:
        return "v"
    elif month == 11:
        return "x"
    elif month == 12:
        return "z"
    else:
        raise ValueError(f"unknown month: {month}")


def month_from_futures_month_code(code: str) -> int:
    if code == "f":
        return 1
    elif code == "g":
        return 2
    elif code == "h":
        return 3
    elif code == "j":
        return 4
    elif code == "k":
        return 5
    elif code == "m":
        return 6
    elif code == "n":
        return 7
    elif code == "q":
        return 8
    elif code == "u":
        return 9
    elif code == "v":
        return 10
    elif code == "x":
        return 11
    elif code == "z":
        return 12
    else:
        raise ValueError(f"unknonw month code: {code}")


def contract_list(
    start: datetime, end: datetime, symbol: str, months: str, fmt: str
) -> List[Contract]:

    cur = Contract.front_month(symbol=symbol, months=months, fmt=fmt, time=end)

    contracts = []
    while cur.year() > start.year and cur.month() >= start.month:
        contracts.append(cur)
        cur = cur.previous_contract()

    return contracts
