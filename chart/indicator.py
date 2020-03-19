import pandas as pd
from typing import Tuple


# def simple_moving_average(df: pd.DataFrame, n: int, column: str = "") -> pd.DataFrame:
def simple_moving_average(df: pd.DataFrame, n: int) -> pd.DataFrame:
    # if column == "":
    # column = f"sma{n}"

    # df.loc[:, column] = df.loc[:, "close"].rolling(n).mean()
    # return df

    # return df.loc[:, "close"].rolling(n).mean()
    return df.rolling(n).mean()


def bollinger_band(
    df: pd.DataFrame, n: int, m: float
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # df: pd.DataFrame, n: int, m: float, column: str = "") -> Tuple[pd.DataFrame, pd.DataFrame]:

    # pl: str
    # ml: str

    # if column == "":
    # pl = f"bb{n}{m:+}"
    # ml = f"bb{n}{m * -1.0:+}"
    # else:
    # pl = f"{column}{n}{m:+}"
    # ml = f"{column}{n}{-m:+}"

    # df.loc[:, pl] = df.loc[:, f"sma{n}"] + (df.loc[:, "close"].rolling(n).std() * m)
    # df.loc[:, ml] = df.loc[:, f"sma{n}"] + (df.loc[:, "close"].rolling(n).std() * -m)

    # return df

    # mean = df.loc[:, "close"].rolling(n).mean()
    mean = df.rolling(n).mean()

    # return (
        # mean + (df.loc[:, "close"].rolling(n).std() * m),
        # mean + (df.loc[:, "close"].rolling(n).std() * -m),
    # )
    return (
        mean + (df.rolling(n).std() * m),
        mean + (df.rolling(n).std() * -m),
    )


def relative_strength(
    # df: pd.DataFrame, rdf: pd.DataFrame, column: str = ""
    df: pd.DataFrame,
    rdf: pd.DataFrame,
) -> pd.DataFrame:

    # if column == "":
    # column = "rs"

    # df.loc[:, column] = df.loc[:, "close"] / rdf.loc[:, "close"]
    # return df

    # return df.loc[:, "close"] / rdf.loc[:, "close"]
    return df / rdf
