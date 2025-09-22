import os
import time
import json
import numpy as np
import pandas as pd
import yfinance as yf
import mysql.connector
from datetime import datetime as dt
import matplotlib.dates as mpl_dates

from Signals import Signals
from SupNRes import SupNRes
from Candles import Candles
from plotChart import Chart
from Indicators import Indicators
from saveSQL import SQLDB

pd.options.mode.chained_assignment = None  # default='warn'


class Market:
    def __init__(self, settings, tick):

        dirpath = os.path.dirname(__file__)
        settings = os.path.join(dirpath, settings)
        tick = os.path.join(dirpath, tick)
        self.latest = os.path.join(dirpath, "Latest")

        self.jsonUnload(settings, tick)
        self.main()

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

    def dfCleanUp(self, df):

        df["Date"] = pd.to_datetime(df.index)
        df["Date"] = df["Date"].apply(mpl_dates.date2num)
        return df.loc[:, ["Date", "Open", "High", "Low", "Close", "Volume"]]

    def SQLconnect(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="root", database="chartdb"
        )

        self.cursor = self.db.cursor()

    def main(self):

        self.SQLconnect()
        timeDict = {}

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

        self.db.commit()
        self.db.close()
        self.cursor.close()
