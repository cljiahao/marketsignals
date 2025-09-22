import os
import time
import json
import numpy as np
import pandas as pd
import yfinance as yf
import mysql.connector
import matplotlib.dates as mpl_dates

from Signals import Signals
from SupNRes import SupNRes
from Candles import Candles
from plotChart import Chart
from Indicators import Indicators
from saveJSON import jsonDataBase
from saveSQL import SQLDB


class Market:
    def __init__(self, settings, tick, database):

        dirpath = os.path.dirname(__file__)
        settings = os.path.join(dirpath, settings)
        tick = os.path.join(dirpath, tick)
        database = os.path.join(dirpath, database)

        self.jsonUnload(settings, tick)
        self.main(database)

    def jsonUnload(self, settings, tick):

        with open(settings, "r") as s:
            sett = json.load(s)
            self.SNR = sett["SupNRes"]
            self.Trend = sett["Trend"]
            self.candles = sett["Candles"]
            self.indicators = sett["indicators"]

        with open(tick, "r") as t:
            data = json.load(t)
            self.tickers = data["ticker"]
            self.perInt = data["periodInterval"]

    def get_stock_price(self, ticker, per, inter):

        df = yf.download(ticker, period=per, interval=inter, threads=False)
        if yf.Ticker(ticker).info["country"] != "Singapore":
            df.Close = df["Adj Close"]
        df["Date"] = pd.to_datetime(df.index)
        df["Date"] = df["Date"].apply(mpl_dates.date2num)
        self.df = df.loc[:, ["Date", "Open", "High", "Low", "Close", "Volume"]]

    def SQLconnect(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="root"
        )

        self.cursor = self.db.cursor()

    def main(self, database):

        self.SQLconnect()
        timeDict = {}

        for country in self.tickers:
            for self.ticker in self.tickers[country]:
                for timeframe in self.perInt:
                    try:
                        start = time.time()
                        self.get_stock_price(
                            self.ticker,
                            self.perInt[timeframe][0],
                            self.perInt[timeframe][1],
                        )
                        timeDict["GetStock"] = time.time() - start
                        start = time.time()
                        self.df = Candles(self.df, self.candles).df
                        timeDict["Candles"] = time.time() - start
                        start = time.time()
                        self.df = Indicators(self.df, self.indicators).df
                        timeDict["Indicators"] = time.time() - start
                        start = time.time()
                        self.levels = SupNRes(self.df, self.SNR).levels
                        timeDict["SupNRes"] = time.time() - start
                        start = time.time()
                        self.df = Signals(self.df, self.levels, self.indicators).df
                        timeDict["Signals"] = time.time() - start
                        start = time.time()
                        jsonDataBase(self.df, self.ticker, timeframe, country, database)
                        timeDict["Json"] = time.time() - start
                        start = time.time()
                        LastBuy = self.df.index.get_loc(
                            self.df["Buy"][self.df["Buy"] > 0].index[-1]
                        )
                        LastSell = self.df.index.get_loc(
                            self.df["Sell"][self.df["Sell"] > 0].index[-1]
                        )
                        lastrow = LastBuy if LastBuy > LastSell else LastSell
                        Chart(
                            self.df[0 : lastrow + 1],
                            self.levels,
                            self.indicators,
                            self.candles,
                            self.ticker,
                            timeframe,
                        )
                        timeDict["Chart"] = time.time() - start

                        print(timeDict)
                    except:
                        pass
        self.db.commit()
        self.db.close()
        self.cursor.close()
