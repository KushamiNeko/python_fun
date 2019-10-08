from multiprocessing import Process

import pandas as pd

import fun.chart.interactive
import fun.chart.static

if __name__ == "__main__":

    df = pd.read_csv("/home/neko/Documents/data_source/yahoo/rut_d.csv")
    quotes = df.set_index("Date")

    quotes["5SMA"] = quotes["Close"].rolling(5).mean()
    quotes["20SMA"] = quotes["Close"].rolling(20).mean()
    quotes["50SMA"] = quotes["Close"].rolling(50).mean()
    quotes["200SMA"] = quotes["Close"].rolling(200).mean()

    quotes["BB+15"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * 1.5

    quotes["BB+20"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * 2.0

    quotes["BB+25"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * 2.5

    quotes["BB+30"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * 3.0

    quotes["BB-15"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * -1.5

    quotes["BB-20"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * -2.0

    quotes["BB-25"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * -2.5

    quotes["BB-30"] = quotes["20SMA"] + quotes["Close"].rolling(20).std() * -3.0

    spx = pd.read_csv("/home/neko/Documents/data_source/yahoo/spx_d.csv")
    spx = spx.set_index("Date")

    quotes["RS"] = quotes["Close"] / spx["Close"]

    slices = quotes.loc["2018-01-01":"2019-01-01"]

    sm = static.StaticChart(slices, chart_size="m")
    sl = static.StaticChart(slices, chart_size="l")

    im = interactive.InteractiveChart(slices, chart_size="m")
    il = interactive.InteractiveChart(slices, chart_size="l")

    ps = [
        # Process(target=sm.stocks_price, args=("stocks_m.png",)),
        Process(target=sl.stocks_price, args=("stocks_l.png",)),
        # Process(target=sm.futures_price, args=("futures_m.png",)),
        Process(target=sl.futures_price, args=("futures_l.png",)),
        # Process(target=im.stocks_price, args=("stocks_m.html",)),
        Process(target=il.stocks_price, args=("stocks_l.html",)),
        # Process(target=im.futures_price, args=("futures_m.html",)),
        Process(target=il.futures_price, args=("futures_l.html",)),
    ]

    for p in ps:
        p.start()

    for p in ps:
        p.join()

