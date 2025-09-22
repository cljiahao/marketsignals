import math
import json

class jsonDataBase:
    def __init__(self,df,ticker,timeframe,country,database):
        self.lastFive = df[-5:]
        self.ticker = ticker
        self.timeframe = timeframe
        self.country = country
        self.prep(database)

    def prep(self,database):

        for i in range(len(self.lastFive)):

            Buy =  "" if math.isnan(self.lastFive['Buy'].values[i]) else round(self.lastFive['Buy'].values[i],2)
            Sell = "" if math.isnan(self.lastFive['Sell'].values[i]) else round(self.lastFive['Sell'].values[i],2)

            signal = {"Buy":Buy,"Sell":Sell}

            with open(database, "r+") as f:
                load = json.load(f)
                # Country
                if self.country in load.keys():
                    # Ticker
                    if self.ticker in load[self.country].keys():
                        # TimeFrame
                        if self.timeframe in load[self.country][self.ticker].keys():
                            # Date
                            if self.lastFive.index[i].strftime("%d-%m-%Y") in load[self.country][self.ticker][self.timeframe].keys():
                                load[self.country][self.ticker][self.timeframe][self.lastFive.index[i].strftime("%d-%m-%Y")] = signal
                            else:
                                load[self.country][self.ticker][self.timeframe].update({self.lastFive.index[i].strftime("%d-%m-%Y"):signal})
                        else:
                            load[self.country][self.ticker].update({self.timeframe:{self.lastFive.index[i].strftime("%d-%m-%Y"):signal}})
                    else:
                        load[self.country].update({self.ticker:{self.timeframe:{self.lastFive.index[i].strftime("%d-%m-%Y"):signal}}})
                else:
                    load[self.country] = {self.ticker:{self.timeframe:{self.lastFive.index[i].strftime("%d-%m-%Y"):signal}}}

                f.seek(0)
                json.dump(load, f,indent=4)
        