from datetime import datetime
from typing import cast
from fun.futures.contract import Contract
from fun.utils import pretty, colors


def last_n_trading_days(front: Contract, back: Contract, n: int) -> datetime:
    assert n > 0
    return cast(datetime, front.dataframe().index[-n].to_pydatetime())


def first_of_month(front: Contract, back: Contract) -> datetime:
    df = front.dataframe()
    selector = (df.index.month == df.index[-1].month) & (
        (df.index[-1] - df.index).days < 90
    )

    return cast(datetime, df.loc[selector].index[0].to_pydatetime(),)


def volume_and_open_interest(
    front: Contract, back: Contract, backup_rolling=first_of_month
) -> datetime:

    fdf = front.dataframe()
    bdf = back.dataframe()

    volume = (
        (
            bdf.loc[bdf.index.isin(fdf.index), "volume"]
            >= fdf.loc[fdf.index.isin(bdf.index), "volume"]
        )
        & (bdf.loc[bdf.index.isin(fdf.index), "volume"] != 0)
        & (fdf.loc[fdf.index.isin(bdf.index), "volume"] != 0)
    )

    interest = (
        (
            bdf.loc[bdf.index.isin(fdf.index), "open interest"]
            >= fdf.loc[fdf.index.isin(bdf.index), "open interest"]
        )
        & (bdf.loc[bdf.index.isin(fdf.index), "open interest"] != 0)
        & (fdf.loc[fdf.index.isin(bdf.index), "open interest"] != 0)
    )

    union = None
    if volume.any() and interest.any():
        union = volume & interest
    elif volume.any() and not interest.any():
        union = volume
    elif not volume.any() and interest.any():
        union = interest
    else:
        pretty.color_print(
            colors.PAPER_AMBER_300,
            f"empty volume and open interest in contracts {front.code().upper()} and {back.code().upper()}"
            ", use backup rolling method instead",
        )

        return cast(datetime, backup_rolling(front, back))

    assert union is not None

    selector = (fdf.index.isin(bdf.index)) & ((fdf.index[-1] - fdf.index).days < 90)

    return cast(datetime, fdf.loc[selector].loc[union].index[0].to_pydatetime(),)
