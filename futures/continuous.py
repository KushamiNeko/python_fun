import re
from datetime import datetime
from typing import Optional

import pandas as pd
from fun.data.source import DAILY, FREQUENCY, MONTHLY, WEEKLY, daily_to_monthly, daily_to_weekly
from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    BARCHART,
    CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    contract_list,
)
from fun.futures.rolling import (LastNTradingDays, RATIO, RollingMethod, VolumeAndOpenInterest)
from fun.utils import colors, pretty


class ContinuousContract:
    @classmethod
    def _default_contract_months(cls, symbol: str) -> CONTRACT_MONTHS:
        months: CONTRACT_MONTHS
        if symbol == "cl":
            months = ALL_CONTRACT_MONTHS
        elif symbol == "gc":
            months = EVEN_CONTRACT_MONTHS
        else:
            months = FINANCIAL_CONTRACT_MONTHS

        assert months is not None and months != ""

        return months

    @classmethod
    def _default_rolling_method(cls, symbol: str) -> RollingMethod:
        if symbol == "cl":
            return VolumeAndOpenInterest(
                    backup=LastNTradingDays(offset=8, adjustment_method=RATIO),
                    adjustment_method=RATIO,
            )
        elif symbol == "gc":
            return VolumeAndOpenInterest(
                    backup=LastNTradingDays(offset=27, adjustment_method=RATIO),
                    adjustment_method=RATIO,
            )
        else:
            return LastNTradingDays(offset=4, adjustment_method=RATIO)

    def read(
            self,
            start: datetime,
            end: datetime,
            symbol: str,
            frequency: FREQUENCY,
            contract_months: Optional[CONTRACT_MONTHS] = None,
            rolling_method: Optional[RollingMethod] = None,
    ) -> pd.DataFrame:

        assert re.match(r"^\w+$", symbol) is not None
        assert frequency in (DAILY, WEEKLY)
        # assert frequency in (DAILY, WEEKLY, MONTHLY)

        if contract_months is None:
            contract_months = self._default_contract_months(symbol)

        if rolling_method is None:
            rolling_method = self._default_rolling_method(symbol)

        cs = contract_list(
                start=start,
                end=end,
                symbol=symbol,
                months=contract_months,
                fmt=BARCHART,
                read_data=True,
        )

        cs_length = len(cs)

        if cs_length == 0:
            raise ValueError("empty contract list")
        elif cs_length == 1:
            return cs[0].dataframe()

        rolling_date = rolling_method.rolling_date(cs[1], cs[0])

        link: pd.DataFrame
        for i in range(cs_length):
            df = cs[i].dataframe()
            if i == 0:
                link = df.loc[df.index >= rolling_date].sort_index(ascending=False)
                continue
            else:
                part = df.loc[(df.index < rolling_date)].sort_index(ascending=False)

                columns = ["open", "high", "low", "close"]
                part.loc[:, columns] = rolling_method.adjust(part.loc[:, columns])

                link = link.loc[link.index >= rolling_date].append(part)

                if i + 1 < cs_length:
                    rolling_date = rolling_method.rolling_date(cs[i + 1], cs[i])
                else:
                    p = cs[i].previous_contract(read_data=False)
                    rolling_date = datetime(year=p.year(), month=p.month(), day=1)

        link = link.loc[link.index >= rolling_date]

        assert link is not None

        link = link.sort_index()

        if frequency == WEEKLY:
            link = daily_to_weekly(link)
        elif frequency == MONTHLY:
            link = daily_to_monthly(link)

        length = len(link)

        na = link.isna().any(axis=1)
        if na.any():
            pretty.color_print(
                    colors.PAPER_AMBER_300,
                    f"dropping {len(link.loc[na])} rows containing nan from {symbol.upper()}",
            )

            dropped_length = len(link.loc[na])

            link = link.dropna()

            assert length == len(link) + dropped_length

        return link
