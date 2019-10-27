import json
import os
import re
from datetime import datetime, timedelta, timezone
from multiprocessing import Process

import pandas as pd
from matplotlib import font_manager

import fun.trading.indicator as ind
from fun.chart.interactive import InteractiveChart
from fun.chart.static import StaticChart
from fun.trading.source import Yahoo
from fun.trading.transaction import FuturesTransaction

if __name__ == "__main__":

    df = Yahoo().read(None, None, "rut", "d")

    df = ind.my_simple_moving_average(df)
    df = ind.my_bollinger_bands(df)

    spx = Yahoo().read(None, None, "spx", "d")

    df["rs"] = df["close"] / spx["close"]

    sdf = df.loc["2018-01-01":"2019-01-01"]

    sm = StaticChart(sdf, chart_size="m")
    sl = StaticChart(sdf, chart_size="l")

    # im = InteractiveChart(df, chart_size="m")
    # il = InteractiveChart(sdf, chart_size="l")

    root = os.path.join(os.getenv("HOME"), "Documents/database/json/market_wizards")

    ts = None

    for f in os.listdir(root):
        if not re.match(r"paper_trading_.+", f):
            continue

        with open(os.path.join(root, f), "r") as fc:
            entities = json.load(fc)
            ts = [FuturesTransaction.from_entity(e) for e in entities]

        mts = ts[int(len(ts) / 2.0)]
        if mts.time.year == 2018:
            break
        else:
            ts = None

    # print(ts)

    # print(slices.index.get_loc(ts[0].time))

    # exit(0)

    ps = [
        Process(
            target=StaticChart(
                ind.my_simple_moving_average_extend(df).loc["2018-01-01":"2019-01-01"],
                chart_size="l",
            ).stocks_price,
            args=("stocks_l.png", ts),
        ),
        Process(target=sl.futures_price, args=("futures_l.png", ts)),
        # Process(
            # target=StaticChart(
                # ind.my_simple_moving_average_extend(df).loc["2018-01-01":"2019-01-01"],
                # chart_size="m",
            # ).stocks_price,
            # args=("stocks_m.png", ts),
        # ),
        # Process(target=sm.futures_price, args=("futures_m.png", ts)),
        # Process(
        # target=InteractiveChart(
        # ind.my_simple_moving_average_extend(df).loc["2018-01-01":"2019-01-01"],
        # chart_size="l",
        # ).stocks_price,
        # args=("stocks_l.html",),
        # ),
        # Process(target=il.futures_price, args=("futures_l.html", ts)),
    ]

    for p in ps:
        p.start()

    for p in ps:
        p.join()
