import re
from datetime import datetime
from typing import cast

import pandas as pd

from fun.data.source import DAILY, FREQUENCY, WEEKLY, daily_to_weekly
from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    BARCHART,
    contract_list,
)
from fun.futures.rolling import RollingMethod


class ContinuousContract:
    def _contract_months(self, symbol: str) -> str:
        months = ""
        if symbol in ["cl"]:
            months = ALL_CONTRACT_MONTHS
        elif symbol in ["gc"]:
            months = EVEN_CONTRACT_MONTHS
        else:
            months = FINANCIAL_CONTRACT_MONTHS

        assert months != ""

        return cast(str, months)

    def read(
        self,
        start: datetime,
        end: datetime,
        symbol: str,
        frequency: FREQUENCY,
        rolling_method: RollingMethod,
    ) -> pd.DataFrame:

        assert re.match(r"^\w+$", symbol) is not None
        assert frequency in (DAILY, WEEKLY)
        assert rolling_method is not None

        cs = contract_list(
            start=start,
            end=end,
            symbol=symbol,
            months=self._contract_months(symbol),
            fmt=BARCHART,
            read_data=True,
        )

        cs_length = len(cs)

        link = None
        for i in range(cs_length):
            rolling_date = None
            if i + 1 < cs_length:
                rolling_date = rolling_method.rolling_date(cs[i + 1], cs[i])
            else:
                # rolling_date = rolling_method(cs[i].previous_contract(), cs[i])
                p = cs[i].previous_contract(read_data=False)
                rolling_date = datetime(year=p.year(), month=p.month(), day=1)

            assert rolling_date is not None

            df = cs[i].dataframe()

            # if rolling_date is not None:
            part = df.loc[df.index >= rolling_date].sort_index(ascending=False)
            # else:
            # part = df.sort_index(ascending=False)

            if link is None:
                link = part
            else:
                # link = link.append(part)
                part.loc[:, ["open", "high", "low", "close"]] = rolling_method.adjust(
                    part.loc[:, ["open", "high", "low", "close"]]
                )

                link = link.append(part)

        assert link is not None

        link = link.sort_index()

        if frequency == WEEKLY:
            link = daily_to_weekly(link)

        return link
