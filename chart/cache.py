from datetime import datetime
from typing import cast

import pandas as pd
from fun.utils import colors, pretty


class QuotesCache:
    def __init__(
            self,
            quotes: pd.DataFrame,
            stime: datetime,
            etime: datetime,
    ):

        assert quotes is not None

        self._quotes = quotes

        self.time_slice(stime, etime)

    def exstime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._quotes.index[0])

    def exetime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._quotes.index[-1])

    def stime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._quotes.index[self._sindex])

    def etime(self) -> pd.Timestamp:
        return cast(pd.Timestamp, self._quotes.index[self._eindex])

    def sindex(self) -> int:
        return cast(int, self._sindex)

    def eindex(self) -> int:
        return cast(int, self._eindex)

    def full_quotes(self) -> pd.DataFrame:
        return self._quotes

    def quotes(self) -> pd.DataFrame:
        return self._quotes.iloc[self._sindex: self._eindex + 1]

    def time_slice(self, stime: datetime, etime: datetime) -> None:
        s = self._quotes.loc[stime:etime]

        self._sindex = self._quotes.index.get_loc(s.index[0])
        self._eindex = self._quotes.index.get_loc(s.index[-1])

    def forward(self) -> bool:
        if self._eindex == len(self._quotes) - 1:
            pretty.color_print(colors.PAPER_AMBER_300, "cache is at the last quote")
            return False

        self._sindex += 1
        self._eindex += 1

        return True

    def backward(self) -> bool:
        if self._sindex == 0:
            pretty.color_print(colors.PAPER_AMBER_300, "cache is at the first quote")
            return False

        self._sindex -= 1
        self._eindex -= 1

        return True
