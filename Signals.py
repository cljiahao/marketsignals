import numpy as np

class Signals:
    def __init__(self,df,levels,indi):
        self.df = df
        self.indi = indi
        self.levels = sorted([lvls[1] for lvls in levels])
        self.df["Buy"], self.df["Sell"] = np.nan,np.nan
        self.df["Correction"], self.df["Recession"], self.df["Crash"] = np.nan,np.nan,np.nan
        self.condition()

    def condition(self):

        low = self.df["Low"]
        high = self.df["High"]

        ma20 = self.df[f"SMA_{self.indi['SMA'][0]['length']}"]
        ma50 = self.df[f"SMA_{self.indi['SMA'][1]['length']}"]
        ma100 = self.df[f"SMA_{self.indi['SMA'][2]['length']}"]
        ma200 = self.df[f"SMA_{self.indi['SMA'][3]['length']}"]
        macd = self.df[f"MACD_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"]
        macdhis = self.df[f"MACDh_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"]
        macdsig =  self.df[f"MACDs_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"]

        PosMHis = (macdhis[macdhis>0].mean() + macdhis[macdhis>0].median()) / 2
        NegMHis = (macdhis[macdhis<0].mean() + macdhis[macdhis<0].median()) / 2

        Urng = 1.01
        Lrng = 0.99

        # Market Overall Trend
        correction = low.loc[high.idxmax():high.index[-1]] < high.max() * 0.85
        recession = low.loc[high.idxmax():high.index[-1]] < high.max() * 0.75
        crash = low.loc[high.idxmax():high.index[-1]] < high.max() * 0.65

        # Pre Conditions
        upTrend = (ma50 > ma200) 
        downTrend = (ma50 < ma200) 

        supmacd = (macdsig < 0) & (macd < 0) & (macdsig > macd) & (macdhis.gt(macdhis.shift(1,axis=0)))
        supmacdLim = supmacd & (macdhis.lt(NegMHis))
        resmacd = (macd > 0) & (macdsig > 0) & (macdsig < macd) & (macdhis.lt(macdhis.shift(1,axis=0)))
        resmacdLim = supmacd & (macdhis.gt(PosMHis))

        # UpTrend Buy
        ma20USup = upTrend & (low > ma20*Lrng) & (low < ma20*Urng) & (low.shift(1,axis=0) > low) & (low > ma50)
        ma50USup = (low > ma50*Lrng) & (low < ma50*Urng) & (low.shift(2,axis=0) > low)
        ma100USup = (low > ma100*Lrng) & (low < ma100*Urng) & (low.shift(2,axis=0) > low)
        ma200USup = (low > ma200*Lrng) & (low < ma200*Urng) & (low.shift(2,axis=0) > low)
 
        # DownTrend Buy
        macdDBuy = supmacd & (macd.gt(macd.shift(1,axis=0))) & (macdsig.lt(macdsig.shift(1,axis=0)))
        ma20DSup = (high.lt(ma20)) & (high.lt(ma50)) & (ma20<ma50) & (high.shift(10,axis=0) > low * 1.13)
        goldenCross = upTrend & (ma200.shift(3,axis=0) > ma50.shift(3,axis=0)) 

        # Buy Signal
        buyUCond = ma20USup & supmacd | ma50USup & supmacd | ma100USup & supmacd | ma200USup & supmacd
        buyDCond = ma20DSup
        buyCond = buyDCond | buyUCond | goldenCross
        self.df["Buy"] = np.where(buyCond,low,np.where(self.df["Buy"] != np.nan, self.df["Buy"],np.nan))

        # UpTrend Sell
        macdUSell = resmacd & (macd.lt(macd.shift(1,axis=0))) & (macdsig.gt(macdsig.shift(1,axis=0)))
        ma20USell = (low.gt(ma20)) & (low.gt(ma50)) & (ma20>ma50) & (low.shift(10,axis=0) < high * 0.87)
        deathCross = downTrend & (ma200.shift(3,axis=0) < ma50.shift(3,axis=0))  

        # Downtrend Sell
        ma20DRes = downTrend & (high > ma20*Lrng) & (high < ma20*Urng) & (high.shift(1,axis=0) < high) & (high < ma50)
        ma50DRes = (high > ma50*Lrng) & (high < ma50*Urng) & (high.shift(2,axis=0) < high)
        ma100DRes = (high > ma100*Lrng) & (high < ma100*Urng) & (high.shift(2,axis=0) < high)
        ma200DRes = (high > ma200*Lrng) & (high < ma200*Urng) & (high.shift(2,axis=0) < high)
        
        # Sell Signal
        sellUCond = ma20USell
        sellDCond = ma20DRes & resmacd | ma50DRes & resmacd | ma100DRes & resmacd | ma200DRes & resmacd
        sellCond = sellDCond | sellUCond | deathCross
        self.df["Sell"] = np.where(sellCond,high,np.where(self.df["Sell"] != np.nan, self.df["Sell"],np.nan))

        # For Levels (Support and Resistance) 
        for i in range(1,len(self.levels)):

            SupCandle = (self.levels[i-1] * Lrng < low) & (self.levels[i-1] * Urng > low) 
            ResCandle =  (self.levels[-i] * Lrng < high) & (self.levels[-i] * Urng > high)

            # Buy Signal
            levelBuy = SupCandle & macdDBuy | SupCandle & supmacdLim 
            self.df["Buy"] = np.where(levelBuy,self.levels[i-1],np.where(self.df["Buy"] != np.nan, self.df["Buy"],np.nan))

            # Sell Signal
            levelSell = ResCandle & macdUSell | ResCandle & resmacdLim  
            self.df["Sell"] = np.where(levelSell,self.levels[-i],np.where(self.df["Sell"] != np.nan, self.df["Sell"],np.nan))

            condCorr = correction & SupCandle & supmacd
            self.df["Correction"] = np.where(condCorr,low.min(),np.where(self.df["Correction"] != np.nan, self.df["Correction"],np.nan))
            
            condRec = recession & SupCandle & supmacd
            self.df["Recession"] = np.where(condRec,low.min(),np.where(self.df["Recession"] != np.nan, self.df["Recession"],np.nan))
            
            condCrash = crash & SupCandle & supmacd
            self.df["Crash"] = np.where(condCrash,low.min(),np.where(self.df["Crash"] != np.nan, self.df["Crash"],np.nan))