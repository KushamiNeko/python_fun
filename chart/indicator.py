from typing import Tuple

import pandas as pd


def simple_moving_average(df: pd.DataFrame, n: int) -> pd.DataFrame:
    return df.rolling(n).mean()


def bollinger_band(
    df: pd.DataFrame, n: int, m: float
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    mean = df.rolling(n).mean()

    return (
        mean + (df.rolling(n).std() * m),
        mean + (df.rolling(n).std() * -m),
    )


def relative_strength(df: pd.DataFrame, rdf: pd.DataFrame,) -> pd.DataFrame:
    return df / rdf
