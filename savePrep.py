import math

class savePrep:
    def __init__(self,df,ticker,timeframe,final):
        self.df = df
        self.ticker = ticker
        self.timeframe = timeframe
        self.final = final
        self.prep()

    def prep(self):

        last = self.df[-1:]
        
        Buy =  "" if math.isnan(last['Buy'].values[0]) else round(last['Buy'].values[0],2)
        Sell = "" if math.isnan(last['Sell'].values[0]) else round(last['Sell'].values[0],2)

        if len(self.final) == 0:
            self.final.extend([last.index[0].strftime("%d-%m-%Y"),self.ticker,self.timeframe,Buy,Sell]) 
        else:
            self.final.extend([self.timeframe,Buy,Sell]) 