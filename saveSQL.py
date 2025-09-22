import math

class SQLDB():
    def __init__(self,df,ticker,timeframe,country,cursor):
            self.lastFive = df[-5:]
            self.ticker = ticker
            self.timeframe = timeframe
            self.country = country
            self.cursor = cursor
            self.prep()

    def prep(self):

        for i in range(len(self.lastFive)):

            Buy =  '' if math.isnan(self.lastFive['Buy'].values[i]) else str(round(self.lastFive['Buy'].values[i],2))
            Sell = '' if math.isnan(self.lastFive['Sell'].values[i]) else str(round(self.lastFive['Sell'].values[i],2))

            query = "INSERT IGNORE INTO signals VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE BuySignal=%s, SellSignal=%s"
            self.cursor.execute(query,(self.country,self.ticker,self.timeframe,self.lastFive.index[i].date(),Buy,Sell,Buy,Sell))