import re
from datetime import datetime
from typing import Callable, cast

import pandas as pd

from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    Contract,
    contract_list,
)
from fun.futures.rolling import last_n_trading_days

# ROLLING_METHOD = NewType("ROLLING_METHOD", int)

# LAST_N_TRADING_DAYS = ROLLING_METHOD(0)
# FIRST_OF_MONTH = ROLLING_METHOD(1)
# VOLUME_AND_OPEN_INTEREST = ROLLING_METHOD(2)


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
        frequency: str,
        rolling_method: Callable[
            [Contract, Contract], datetime
        ] = lambda front, back: cast(datetime, last_n_trading_days(front, back, n=4)),
        # adjusting_method: Callable[[datetime, Contract, Contract], pd.DataFrame],
        # rolling_method: ROLLING_METHOD = LAST_N_TRADING_DAYS,
        # rolling_parameters: Optional[Dict[str, Any]] = None,
    ) -> pd.DataFrame:

        assert re.match(r"^\w+$", symbol) is not None
        assert frequency in ("d", "w")
        assert rolling_method is not None

        # assert rolling_method in (
        # LAST_N_TRADING_DAYS,
        # FIRST_OF_MONTH,
        # VOLUME_AND_OPEN_INTEREST,
        # )

        cs = contract_list(
            start=start,
            end=end,
            symbol=symbol,
            months=self._contract_months(symbol),
            fmt="barchart",
            read_data=True,
        )

        cs_length = len(cs)

        link = None
        for i in range(cs_length):
            rolling_date = None
            try:
                if i + 1 < cs_length:
                    rolling_date = rolling_method(cs[i + 1], cs[i])
                else:
                    rolling_date = rolling_method(cs[i].previous_contract(), cs[i])
            except FileNotFoundError:
                rolling_date = None

            df = cs[i].dataframe()

            if rolling_date is not None:
                part = df.loc[df.index >= rolling_date].sort_index(ascending=False)
            else:
                part = df.sort_index(ascending=False)

            if link is None:
                link = part
            else:
                link = link.append(part)

        assert link is not None

        return link.sort_index()


if __name__ == "__main__":
    c = ContinuousContract()
    df = c.read(
        datetime.strptime("20190101", "%Y%m%d"),
        datetime.strptime("20200101", "%Y%m%d"),
        "es",
        "d",
    )

    print(df)
