import os
import time
import json
import pandas as pd
import yfinance as yf
import matplotlib.dates as mpl_dates

from Signals import Signals
from SupNRes import SupNRes
from Candles import Candles
from plotChart import Chart
from Indicators import Indicators
from savePrep import savePrep
from Database import Database

class Market():
    def __init__(self,settings,tick):

        dirpath = os.path.dirname(__file__)
        settings = os.path.join(dirpath,settings)
        tick = os.path.join(dirpath,tick)

        self.jsonUnload(settings,tick)
        self.main()

    def jsonUnload(self,settings,tick):

        with open(settings, 'r') as s:
            sett = json.load(s)
            self.SNR = sett["SupNRes"]
            self.Trend = sett["Trend"]
            self.candles = sett["Candles"]
            self.indicators = sett["indicators"]

        with open(tick, 'r') as t:
            data = json.load(t)
            self.tickers = data["ticker"]
            self.perInt = data["periodInterval"]

    def get_stock_price(self,ticker,per,inter):

        df = yf.download(ticker, period=per, interval=inter, threads= False)
        if yf.Ticker(ticker).info['country'] != "Singapore": df.Close = df['Adj Close']
        df['Date'] = pd.to_datetime(df.index)
        df['Date'] = df['Date'].apply(mpl_dates.date2num)
        self.df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close','Volume']]

    def main(self):

        for country in self.tickers:
            for self.ticker in self.tickers[country]:
                final = []
                for timeframe in self.perInt:
                    try:
                        self.get_stock_price(self.ticker,self.perInt[timeframe][0],self.perInt[timeframe][1])
                        self.df = Candles(self.df,self.candles).df
                        self.df = Indicators(self.df,self.indicators).df
                        self.levels = SupNRes(self.df,self.SNR).levels
                        self.df = Signals(self.df,self.levels,self.indicators).df
                        final = savePrep(self.df,self.ticker,timeframe,final).final
                        Chart(self.df,self.levels,self.indicators,self.candles,self.ticker,timeframe)
                    except:
                        pass

                Database(final,country)
                


