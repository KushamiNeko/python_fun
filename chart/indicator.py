from typing import Optional, Tuple

import pandas as pd


def my_simple_moving_average(df: pd.DataFrame) -> pd.DataFrame:
    df = simple_moving_average(df, 5)
    df = simple_moving_average(df, 20)

    return df


def my_simple_moving_average_extend(df: pd.DataFrame) -> pd.DataFrame:
    df = simple_moving_average(df, 50)
    df = simple_moving_average(df, 200)

    return df


def my_bollinger_bands(df: pd.DataFrame) -> pd.DataFrame:
    df = bollinger_bands(df, 20, 1.5)
    df = bollinger_bands(df, 20, 2.0)
    df = bollinger_bands(df, 20, 2.5)
    df = bollinger_bands(df, 20, 3.0)

    return df


def simple_moving_average(
    df: pd.DataFrame, n: int, label: Optional[str] = None
) -> pd.DataFrame:

    if label is None:
        label = f"sma{n}"

    df[label] = df["close"].rolling(n).mean()
    return df


def bollinger_bands(
    df: pd.DataFrame, n: int, m: float, labels: Optional[Tuple[str, str]] = None
) -> pd.DataFrame:

    pl: str
    ml: str

    if labels is None:
        pl = f"bb{n}{m:+}"
        ml = f"bb{n}{m * -1.0:+}"

    else:
        pl = labels[0]
        ml = labels[1]

    df[pl] = df[f"sma{n}"] + df["close"].rolling(n).std() * m
    df[ml] = df[f"sma{n}"] + df["close"].rolling(n).std() * m * -1.0

    return df


def relative_strength(
    df: pd.DataFrame, rdf: pd.DataFrame, label: Optional[str]
) -> pd.DataFrame:

    if label is None:
        label = "rs"

    df[label] = df["close"] / rdf["close"]
    return df
