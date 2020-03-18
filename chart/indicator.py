import pandas as pd


def simple_moving_average(df: pd.DataFrame, n: int, column: str = "") -> pd.DataFrame:
    if column == "":
        column = f"sma{n}"

    df.loc[:, column] = df.loc[:, "close"].rolling(n).mean()
    return df


def bollinger_band(
    df: pd.DataFrame, n: int, m: float, column: str = ""
) -> pd.DataFrame:

    pl: str
    ml: str

    if column == "":
        pl = f"bb{n}{m:+}"
        ml = f"bb{n}{m * -1.0:+}"
    else:
        pl = f"{column}{n}{m:+}"
        ml = f"{column}{n}{-m:+}"

    df.loc[:, pl] = df.loc[:, f"sma{n}"] + (df.loc[:, "close"].rolling(n).std() * m)
    df.loc[:, ml] = df.loc[:, f"sma{n}"] + (df.loc[:, "close"].rolling(n).std() * -m)

    return df


def relative_strength(
    df: pd.DataFrame, rdf: pd.DataFrame, column: str = ""
) -> pd.DataFrame:

    if column == "":
        column = "rs"

    df.loc[:, column] = df.loc[:, "close"] / rdf.loc[:, "close"]
    return df
