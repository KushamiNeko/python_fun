import json
import os
import re
from datetime import datetime
from multiprocessing import Process

import pandas as pd
from matplotlib import font_manager

from fun.chart.interactive import InteractiveChart
from fun.chart.static import StaticChart
from fun.trading.transaction import FuturesTransaction

# for f in font_manager.fontManager.ttflist:
    # print(f.name)


if __name__ == "__main__":

    df = pd.read_csv("/home/neko/Documents/data_source/yahoo/rut_d.csv")

    cols = {k: k.lower() for k in df.columns}

    df = df.rename(columns=cols)

    df["date"] = df["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

    quotes = df.set_index("date")

    quotes["5sma"] = quotes["close"].rolling(5).mean()
    quotes["20sma"] = quotes["close"].rolling(20).mean()
    quotes["50sma"] = quotes["close"].rolling(50).mean()
    quotes["200sma"] = quotes["close"].rolling(200).mean()

    quotes["bb+15"] = quotes["20sma"] + quotes["close"].rolling(20).std() * 1.5

    quotes["bb+20"] = quotes["20sma"] + quotes["close"].rolling(20).std() * 2.0

    quotes["bb+25"] = quotes["20sma"] + quotes["close"].rolling(20).std() * 2.5

    quotes["bb+30"] = quotes["20sma"] + quotes["close"].rolling(20).std() * 3.0

    quotes["bb-15"] = quotes["20sma"] + quotes["close"].rolling(20).std() * -1.5

    quotes["bb-20"] = quotes["20sma"] + quotes["close"].rolling(20).std() * -2.0

    quotes["bb-25"] = quotes["20sma"] + quotes["close"].rolling(20).std() * -2.5

    quotes["bb-30"] = quotes["20sma"] + quotes["close"].rolling(20).std() * -3.0

    spx = pd.read_csv("/home/neko/Documents/data_source/yahoo/spx_d.csv")
    cols = {k: k.lower() for k in spx.columns}
    spx = spx.rename(columns=cols)

    spx["date"] = spx["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

    spx = spx.set_index("date")

    quotes["rs"] = quotes["close"] / spx["close"]

    slices = quotes.loc["2018-01-01":"2019-01-01"]

    sm = StaticChart(slices, chart_size="m")
    sl = StaticChart(slices, chart_size="l")

    im = InteractiveChart(slices, chart_size="m")
    il = InteractiveChart(slices, chart_size="l")

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
        # Process(target=sm.stocks_price, args=("stocks_m.png",)),
        # Process(target=sl.stocks_price, args=("stocks_l.png", ts)),
        # Process(target=sm.futures_price, args=("futures_m.png",)),
        Process(target=sl.futures_price, args=("futures_l.png", ts)),
        # Process(target=im.stocks_price, args=("stocks_m.html",)),
        # Process(target=il.stocks_price, args=("stocks_l.html",)),
        # Process(target=im.futures_price, args=("futures_m.html",)),
        Process(target=il.futures_price, args=("futures_l.html", ts)),
    ]

    for p in ps:
        p.start()

    for p in ps:
        p.join()
