import re
from typing import Optional
from datetime import datetime

import pandas as pd

from fun.data import continuous

# BarchartSymbolFormat SymbolFormat = iota
# QuandlSymbolFormat

# AllContractMonths  ContractMonths = "fghjkmnquvxz"
# EvenContractMonths ContractMonths = "gjmqvz"

# FinancialContractMonths ContractMonths = "hmuz"

# LastNTradingDay RollingMethod = iota
# FirstOfMonth
# OpenInterest

# PanamaCanal AdjustingMethod = iota
# Ratio

# barchartContractPattern = `(\w{2})([fghjkmnquvxz])(\d{2})`
# quandlContractPattern   = `([\d\w]+)([fghjkmnquvxz])(\d{4})`


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


class Contract:
    def __init__(
        self, symbol: str, fmt: str, df: Optional[pd.DataFrame], read_data: bool = True
    ) -> None:

        assert fmt in ("barchart", "quandl")

        self._df = df
        if read_data:
            self.read_contract_data()

        self._symbol = symbol
        self._fmt = fmt

        year = 0
        month = 0
        if self._fmt == "barchart":
            match = re.match(self._barchart_symbol_format, self._symbol)
            if match is None:
                raise ValueError(
                    f"invalid symbol {self._symbol} for {self._fmt} format"
                )

            year = int(f"20{match.group(3)}")
            month = month_from_futures_month_code(match.group(2))

        elif self._fmt == "quandl":
            match = re.match(self._quandl_symbol_format, self._symbol)
            if match is None:
                raise ValueError(
                    f"invalid symbol {self._symbol} for {self._fmt} format"
                )

            year = int(match.group(3))
            month = month_from_futures_month_code(match.group(2))

        else:
            raise ValueError("unknown symbol format: {self._fmt}")

        assert year != 0
        assert month != 0

        if year > datetime.now().year:
            year -= 100

        self._year = year
        self._month = month

    @property
    def _barchart_symbol_format(self) -> str:
        return r"(\w{2})([fghjkmnquvxz])(\d{2})"

    @property
    def _quandl_symbol_format(self) -> str:
        return r"([\d\w]+)([fghjkmnquvxz])(\d{4})"

    def read_contract_data(self) -> None:
        src = continuous.Contract()
        self._df = src.read(datetime(1776, 7, 4), datetime.now(), self._symbol, "d")
        assert self._df is not None

    def contract_year(self) -> int:
        return self._year

    def contract_month(self) -> int:
        return self._month
