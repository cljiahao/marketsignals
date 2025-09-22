import numpy as np

class Signals:
    def __init__(self,df,levels,indi):
        self.df = df
        self.indi = indi
        self.levels = sorted([lvls[1] for lvls in levels])
        self.df['preBuy'], self.df['preSell'] = np.nan,np.nan
        self.df["Correction"], self.df["Recession"], self.df["Crash"] = np.nan,np.nan,np.nan
        self.condition()
        self.BuysellClean()

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
        
        supmacd = (macdsig > macd) & (macdhis.gt(macdhis.shift(1,axis=0)))
        supDmacd = (macdsig < 0) & (macd < 0) & supmacd
        supmacdLim = supDmacd & (macdhis.lt(NegMHis))
        resmacd = (macdsig < macd) & (macdhis.lt(macdhis.shift(1,axis=0)))
        resUmacd = (macd > 0) & (macdsig > 0) & resmacd
        resmacdLim = resUmacd & (macdhis.gt(PosMHis))

        # UpTrend Buy
        ma20USup = upTrend & (low > ma20*Lrng) & (low < ma20*Urng) & ((low.shift(1,axis=0) > low) | (low.shift(2,axis=0) > low)) & (low > ma50)
        ma50USup = (low > ma50*Lrng) & (low < ma50*Urng) & ((low.shift(1,axis=0) > low) | (low.shift(2,axis=0) > low)) & (low > ma100)
        ma100USup = (low > ma100*Lrng) & (low < ma100*Urng) & ((low.shift(1,axis=0) > low) | (low.shift(2,axis=0) > low)) & (low > ma200)
        ma200USup = (low > ma200*Lrng) & (low < ma200*Urng) & ((low.shift(1,axis=0) > low) | (low.shift(2,axis=0) > low)) & (ma50 > ma200)
 
        # DownTrend Buy
        macdDBuy = supDmacd & (macd.gt(macd.shift(1,axis=0))) & (macdsig.lt(macdsig.shift(1,axis=0))) & (macd.gt(macd.shift(2,axis=0))) & (macdsig.lt(macdsig.shift(2,axis=0)))
        goldenCross = upTrend & (ma200.shift(3,axis=0) > ma50.shift(3,axis=0)) 

        # Buy Signal
        buyUCond = ma20USup & supDmacd | ma50USup & supDmacd | ma100USup & supDmacd | ma200USup & supDmacd
        buyDCond = macdDBuy
        buyCond = buyDCond | buyUCond
        self.df['preBuy'] = np.where(buyCond,low,np.where(self.df['preBuy'] != np.nan, self.df['preBuy'],np.nan))

        # UpTrend Sell
        macdUSell = resUmacd & (macd.lt(macd.shift(1,axis=0))) & (macdsig.gt(macdsig.shift(1,axis=0))) & (macd.lt(macd.shift(2,axis=0))) & (macdsig.gt(macdsig.shift(2,axis=0)))
        deathCross = downTrend & (ma200.shift(3,axis=0) < ma50.shift(3,axis=0))  

        # Downtrend Sell
        ma20DRes = downTrend & (high > ma20*Lrng) & (high < ma20*Urng) & ((high.shift(1,axis=0) < high) | (high.shift(2,axis=0) < high)) & (high < ma50)
        ma50DRes = (high > ma50*Lrng) & (high < ma50*Urng) & ((high.shift(1,axis=0) < high) | (high.shift(2,axis=0) < high)) & (high < ma100)
        ma100DRes = (high > ma100*Lrng) & (high < ma100*Urng) & ((high.shift(1,axis=0) < high) | (high.shift(2,axis=0) < high)) & (high < ma200)
        ma200DRes = (high > ma200*Lrng) & (high < ma200*Urng) & ((high.shift(1,axis=0) < high) | (high.shift(2,axis=0) < high)) & (ma50 < ma200)
        
        # Sell Signal
        sellUCond = macdUSell
        sellDCond = ma20DRes & resUmacd | ma50DRes & resUmacd | ma100DRes & resUmacd | ma200DRes & resUmacd
        sellCond = sellDCond | sellUCond
        self.df['preSell'] = np.where(sellCond,high,np.where(self.df['preSell'] != np.nan, self.df['preSell'],np.nan))

        # For Levels (Support and Resistance) 
        for i in range(1,len(self.levels)):

            SupCandle = (self.levels[i-1] * Lrng < low) & (self.levels[i-1] * Urng > low) 
            ResCandle =  (self.levels[-i] * Lrng < high) & (self.levels[-i] * Urng > high)

            # Buy Signal
            levelBuy = SupCandle & buyDCond | SupCandle & buyUCond | SupCandle & supmacdLim | SupCandle & ma200USup & supmacd
            self.df['preBuy'] = np.where(levelBuy,self.levels[i-1],np.where(self.df['preBuy'] != np.nan, self.df['preBuy'],np.nan))

            # Sell Signal
            levelSell = ResCandle & sellUCond | ResCandle & sellDCond | ResCandle & resmacdLim | ResCandle & ma200DRes & resmacd
            self.df['preSell'] = np.where(levelSell,self.levels[-i],np.where(self.df['preSell'] != np.nan, self.df['preSell'],np.nan))

            condCorr = correction & SupCandle & supDmacd
            self.df["Correction"] = np.where(condCorr,low.min(),np.where(self.df["Correction"] != np.nan, self.df["Correction"],np.nan))
            
            condRec = recession & SupCandle & supDmacd
            self.df["Recession"] = np.where(condRec,low.min(),np.where(self.df["Recession"] != np.nan, self.df["Recession"],np.nan))
            
            condCrash = crash & SupCandle & supDmacd
            self.df["Crash"] = np.where(condCrash,low.min(),np.where(self.df["Crash"] != np.nan, self.df["Crash"],np.nan))

    def BuysellClean(self):

        self.df['Buy'],self.df['Sell'] = np.nan,np.nan

        dur = 5
        Max, Min = [],[]
        for i in range(dur, len(self.df)-dur):
            # WinShift for High Range 
            high_range = self.df['preSell'][i-dur:i+dur-1]
            current_max = high_range.max()
            if current_max not in Max: Max = []
            Max.append(current_max)
            if (len(Max) == dur or i == (len(self.df)-dur-1)) and not np.isnan(Max).all():
                self.df['Sell'][high_range.idxmax()] = max(Max)

            # WinShift for Low Range 
            low_range = self.df['preBuy'][i-dur:i+dur]
            current_min = low_range.min()
            if current_min not in Min: Min = []
            Min.append(current_min)
            if (len(Min) == dur or i == (len(self.df)-dur-1)) and not np.isnan(Min).all():
                self.df['Buy'][low_range.idxmin()] = min(Min)