import os
import time
import json
import numpy as np
import pandas as pd
import yfinance as yf
import mysql.connector
<<<<<<< HEAD
=======
from datetime import datetime as dt
>>>>>>> v3
import matplotlib.dates as mpl_dates

from Signals import Signals
from SupNRes import SupNRes
from Candles import Candles
from plotChart import Chart
from Indicators import Indicators
<<<<<<< HEAD
from saveJSON import jsonDataBase
from saveSQL import SQLDB


class Market:
    def __init__(self, settings, tick, database):
=======
from saveSQL import SQLDB

pd.options.mode.chained_assignment = None  # default='warn'


class Market:
    def __init__(self, settings, tick):
>>>>>>> v3

        dirpath = os.path.dirname(__file__)
        settings = os.path.join(dirpath, settings)
        tick = os.path.join(dirpath, tick)
<<<<<<< HEAD
        database = os.path.join(dirpath, database)

        self.jsonUnload(settings, tick)
        self.main(database)
=======
        self.latest = os.path.join(dirpath, "Latest")

        self.jsonUnload(settings, tick)
        self.main()
>>>>>>> v3

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

<<<<<<< HEAD
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
=======
    def dfCleanUp(self, df):

        df["Date"] = pd.to_datetime(df.index)
        df["Date"] = df["Date"].apply(mpl_dates.date2num)
        return df.loc[:, ["Date", "Open", "High", "Low", "Close", "Volume"]]

    def SQLconnect(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="root", database="chartdb"
>>>>>>> v3
        )

        self.cursor = self.db.cursor()

<<<<<<< HEAD
    def main(self, database):
=======
    def main(self):
>>>>>>> v3

        self.SQLconnect()
        timeDict = {}

<<<<<<< HEAD
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
=======
        for timeframe in self.perInt:
            for country in self.tickers:
                start = time.time()
                df = yf.download(
                    list(self.tickers[country].values()),
                    period=self.perInt[timeframe][0],
                    interval=self.perInt[timeframe][1],
                    group_by="ticker",
                    auto_adjust=True,
                )
                timeDict["GetStock"] = time.time() - start
                for name, ticker in self.tickers[country].items():
                    try:
                        start = time.time()
                        subdf = self.dfCleanUp(df[ticker])
                        subdf = Candles(subdf, self.candles).df
                        timeDict["Candles"] = time.time() - start
                        start = time.time()
                        subdf = Indicators(subdf, self.indicators).df
                        timeDict["Indicators"] = time.time() - start
                        start = time.time()
                        self.levels = SupNRes(subdf, self.SNR).levels
                        timeDict["SupNRes"] = time.time() - start
                        start = time.time()
                        subdf = Signals(subdf, self.levels, self.indicators).df
                        timeDict["Signals"] = time.time() - start
                        start = time.time()
                        SQLDB(subdf, name, timeframe, country, self.cursor)
                        timeDict["SQL"] = time.time() - start
                        start = time.time()
                        Chart(
                            subdf,
                            self.levels,
                            self.indicators,
                            self.candles,
                            os.path.join(
                                self.latest,
                                name
                                + "_"
                                + timeframe
                                + "_"
                                + str(dt.today().year)
                                + ".png",
                            ),
                        )
                        # LastBuy = subdf.index.get_loc(subdf["Buy"][subdf["Buy"]>0].index[-1])
                        # LastSell = subdf.index.get_loc(subdf["Sell"][subdf["Sell"]>0].index[-1])
                        # lastrow = LastBuy if LastBuy > LastSell else LastSell
                        # date = subdf[0:lastrow+1].index[-1].strftime("%d-%m-%Y")
                        # Chart(subdf[0:lastrow+1],self.levels,self.indicators,self.candles,os.path.join(self.folpath,date+"_"+name+"_"+timeframe+".png"))
                        timeDict["Chart"] = time.time() - start
                        print(timeDict)
                    except:
                        print(f"{ticker} -> Error")
                        pass

>>>>>>> v3
        self.db.commit()
        self.db.close()
        self.cursor.close()
