import numpy as np

<<<<<<< HEAD
class Candles():
    def __init__(self,df,candles):
        self.df = df
        self.candles = candles if len(candles) != 0 else ["Hammers","Stars","RiseNFall","ThreeLineStrike","Engulfing"]
=======

class Candles:
    def __init__(self, df, candles):
        self.df = df
        self.candles = (
            candles
            if len(candles) != 0
            else ["Hammers", "Stars", "RiseNFall", "ThreeLineStrike", "Engulfing"]
        )
>>>>>>> v3
        self.prepCandle()
        self.main()

    def prepCandle(self):

        self.Low = self.df["Low"]
<<<<<<< HEAD
        self.Low1 = self.Low.shift(1,axis=0)
        self.Low2 = self.Low.shift(2,axis=0)

        self.High = self.df["High"]
        self.High1 = self.High.shift(1,axis=0)
        self.High2 = self.High.shift(2,axis=0)

        self.Open = self.df["Open"]
        self.Open1 = self.Open.shift(1,axis=0)
        self.Open2 = self.Open.shift(2,axis=0)
        self.Open3 = self.Open.shift(3,axis=0)
        self.Open4 = self.Open.shift(4,axis=0)

        self.Close = self.df["Close"]
        self.Close1 = self.Close.shift(1,axis=0)
        self.Close2 = self.Close.shift(2,axis=0)
        self.Close3 = self.Close.shift(3,axis=0)
        self.Close4 = self.Close.shift(4,axis=0)

    def ThreeLineStrike(self):

        bull123 = (self.Close1>self.Open1) & (self.Close2>self.Open2) & (self.Close3>self.Open3) & (self.Open1>self.Open2) & (self.Open2>self.Open3)
        bull4 = (self.Open3>self.Close) & (self.Open>self.Close1)
        bull = bull123 & bull4
        self.df["BullTLS"] = np.where(bull,self.Low,np.nan)

        bear123 = (self.Close1<self.Open1) & (self.Close2<self.Open2) & (self.Close3<self.Open3) & (self.Open1<self.Open2) & (self.Open2<self.Open3)
        bear4 = (self.Open3<self.Close) & (self.Open<self.Close1)
        bear = bear123 & bear4
        self.df["BearTLS"] = np.where(bear,self.High,np.nan)       
=======
        self.Low1 = self.Low.shift(1, axis=0)
        self.Low2 = self.Low.shift(2, axis=0)

        self.High = self.df["High"]
        self.High1 = self.High.shift(1, axis=0)
        self.High2 = self.High.shift(2, axis=0)

        self.Open = self.df["Open"]
        self.Open1 = self.Open.shift(1, axis=0)
        self.Open2 = self.Open.shift(2, axis=0)
        self.Open3 = self.Open.shift(3, axis=0)
        self.Open4 = self.Open.shift(4, axis=0)

        self.Close = self.df["Close"]
        self.Close1 = self.Close.shift(1, axis=0)
        self.Close2 = self.Close.shift(2, axis=0)
        self.Close3 = self.Close.shift(3, axis=0)
        self.Close4 = self.Close.shift(4, axis=0)

    def ThreeLineStrike(self):

        bull123 = (
            (self.Close1 > self.Open1)
            & (self.Close2 > self.Open2)
            & (self.Close3 > self.Open3)
            & (self.Open1 > self.Open2)
            & (self.Open2 > self.Open3)
        )
        bull4 = (self.Open3 > self.Close) & (self.Open > self.Close1)
        bull = bull123 & bull4
        self.df["BullTLS"] = np.where(bull, self.Low, np.nan)

        bear123 = (
            (self.Close1 < self.Open1)
            & (self.Close2 < self.Open2)
            & (self.Close3 < self.Open3)
            & (self.Open1 < self.Open2)
            & (self.Open2 < self.Open3)
        )
        bear4 = (self.Open3 < self.Close) & (self.Open < self.Close1)
        bear = bear123 & bear4
        self.df["BearTLS"] = np.where(bear, self.High, np.nan)
>>>>>>> v3

    def Stars(self):

        body = 2
        wick = 0.7

<<<<<<< HEAD
        morn12 = ((self.Open2-self.Close2)>0) & ((abs(self.Open1-self.Close1)*body).lt(self.Open2-self.Close2)) 
        morn23 = ((self.Close-self.Open)>0) & ((abs(self.Open1-self.Close1)*body).lt(self.Close-self.Open))
        morn2 = np.where(self.Open1<self.Close1,(self.High1-self.Close1).between((self.Open1-self.Low1)*wick,(self.Open1-self.Low1)),(self.High1-self.Open1).between((self.Close1-self.Low1)*wick,(self.Close1-self.Low1)))
        morn123 = (self.Low2.gt(self.Low1)) & (self.Low1.lt(self.Low)) & morn2 & morn12 & morn23
        self.df["morning"] = np.where(morn123,self.Low,np.nan)

        even12 = ((self.Close2-self.Open2)>0) & ((abs(self.Close1-self.Open1)*body).lt(self.Close2-self.Open2))
        even23 = ((self.Open-self.Close)>0) & ((abs(self.Close1-self.Open1)*body).lt(self.Open-self.Close))
        even2 = np.where(self.Open1<self.Close1,(self.High1-self.Close1).between((self.Open1-self.Low1)*wick,(self.Open1-self.Low1)),(self.High1-self.Open1).between((self.Close1-self.Low1)*wick,(self.Close1-self.Low1)))
        even123 = (self.High2.lt(self.High1)) & (self.High1.gt(self.High)) & even2 & even12 & even23
        self.df["evening"] = np.where(even123,self.High,np.nan)

    def Hammers(self):

        cond1 = np.where(self.Open2<self.Close2,self.Open2,self.Close2)
        cond2 = np.where(self.Open<self.Close,self.Open,self.Close)

        body = 2
        wick = 0.7
        
        ham12 = ((self.Open2-self.Close2)>0) & ((abs(self.Open1-self.Close1)*body).lt(self.Open2-self.Close2)) 
        ham23 = ((self.Close-self.Open)>0) & ((abs(self.Open1-self.Close1)*body).lt(self.Close-self.Open))
        ham2 = np.where(self.Open1<self.Close1,self.Close1.between(self.High1*wick,self.High1),self.Open1.between(self.High1*wick,self.High1)) & (abs(self.Open1-self.Close1)*body<self.High1-self.Low1)
        ham123 = (self.Low2.gt(self.Low1)) & (self.Low1.lt(self.Low)) & np.where(self.Open1<self.Close1,(self.Open1.lt(cond1)) & (self.Open1.lt(cond2)),(self.Close1.lt(cond1)) & (self.Close1.lt(cond2))) & ham2 & ham12 & ham23 
        self.df["hammer"] = np.where(ham123,self.Low,np.nan)

        invham12 = ((self.Open2-self.Close2)>0) & ((abs(self.Open1-self.Close1)*body).lt(self.Open2-self.Close2)) 
        invham23 = ((self.Close-self.Open)>0) & ((abs(self.Open1-self.Close1)*body).lt(self.Close-self.Open))
        invham2 = np.where(self.Open1<self.Close1,self.Open1.between(self.Low1*wick,self.Low1),self.Close1.between(self.Low1*wick,self.Low1)) & (abs(self.Open1-self.Close1)*body<self.High1-self.Low1)
        invham123 = (self.Low2.gt(self.Low1)) & (self.Low1.lt(self.Low)) & np.where(self.Open1<self.Close1,(self.Open1.lt(cond1)) & (self.Open1.lt(cond2)),(self.Close1.lt(cond1)) & (self.Close1.lt(cond2))) & invham2 & invham12 & invham23
        self.df["invhammer"] = np.where(invham123,self.Low,np.nan)

        hang12 = ((self.Close2-self.Open2)>0) & ((abs(self.Close1-self.Open1)*body).lt(self.Close2-self.Open2))
        hang23 = ((self.Open-self.Close)>0) & ((abs(self.Close1-self.Open1)*body).lt(self.Open-self.Close))
        hang2 = np.where(self.Open1<self.Close1,self.Close1.between(self.High1*wick,self.High1),self.Open1.between(self.High1*wick,self.High1)) & (abs(self.Open1-self.Close1)*body<self.High1-self.Low1)
        hang123 = (self.High2.lt(self.High1)) & (self.High1.gt(self.High)) & np.where(self.Open1<self.Close1,(self.Close1.gt(cond1)) & (self.Close1.gt(cond2)),(self.Open1.gt(cond1)) & (self.Open1.gt(cond2))) & hang2 & hang12 & hang23
        self.df["hanging"] = np.where(hang123,self.High,np.nan)

        shoot12 = ((self.Close2-self.Open2)>0) & ((abs(self.Close1-self.Open1)*body).lt(self.Close2-self.Open2))
        shoot23 = ((self.Open-self.Close)>0) & ((abs(self.Close1-self.Open1)*body).lt(self.Open-self.Close))
        shoot2 = np.where(self.Open1<self.Close1,self.Open1.between(self.Low1*wick,self.Low1),self.Close1.between(self.Low1*wick,self.Low1)) & (abs(self.Open1-self.Close1)*body<self.High1-self.Low1)
        shoot123 = (self.High2.lt(self.High1)) & (self.High1.gt(self.High)) & np.where(self.Open1<self.Close1,(self.Close1.gt(cond1)) & (self.Close1.gt(cond2)),(self.Open1.gt(cond1)) & (self.Open1.gt(cond2))) & shoot2 & shoot12 & shoot23
        self.df["shooting"] = np.where(shoot123,self.High,np.nan)

    def RiseNFall(self):

        rise234 = (self.Open3>self.Close3) & (self.Open2>self.Close2) & (self.Open1>self.Close1) & (self.Open3>self.Open2) & (self.Open2>self.Open1)
        rise1 = (self.Close4>=self.Open3) & (self.Open4<=self.Close1) & (self.Close4>self.Open4)
        rise5 = (self.Close>self.Close4) & (self.Close>self.Open)
        rising = rise1 & rise234 & rise5
        self.df["rising"] = np.where(rising,self.Low,np.nan)

        fall234 = (self.Open3<self.Close3) & (self.Open2<self.Close2) & (self.Open1<self.Close1) & (self.Open3<self.Open2) & (self.Open2<self.Open1)
        fall1 = (self.Close4<=self.Open3) & (self.Open4>=self.Close1) & (self.Close4<self.Open4)
        fall5 = (self.Close<self.Close4) & (self.Close<self.Open)
        falling = fall1 & fall234 & fall5
        self.df["falling"] = np.where(falling,self.High,np.nan)

    def Engulfing(self):

        bullish = (self.Open.lt(self.Close1)) & (self.Close.gt(self.Open1)) & (self.Open1>self.Close1)
        self.df["bullEngulf"] = np.where(bullish,self.Low,np.nan)

        bearish = (self.Close.lt(self.Open1)) & (self.Open.gt(self.Close1)) & (self.Open1<self.Close1)
        self.df["bearEngulf"] = np.where(bearish,self.High,np.nan)

    def main(self):
        for i in self.candles:
            getattr(self,i)()
=======
        morn12 = ((self.Open2 - self.Close2) > 0) & (
            (abs(self.Open1 - self.Close1) * body).lt(self.Open2 - self.Close2)
        )
        morn23 = ((self.Close - self.Open) > 0) & (
            (abs(self.Open1 - self.Close1) * body).lt(self.Close - self.Open)
        )
        morn2 = np.where(
            self.Open1 < self.Close1,
            (self.High1 - self.Close1).between(
                (self.Open1 - self.Low1) * wick, (self.Open1 - self.Low1)
            ),
            (self.High1 - self.Open1).between(
                (self.Close1 - self.Low1) * wick, (self.Close1 - self.Low1)
            ),
        )
        morn123 = (
            (self.Low2.gt(self.Low1))
            & (self.Low1.lt(self.Low))
            & morn2
            & morn12
            & morn23
        )
        self.df["morning"] = np.where(morn123, self.Low, np.nan)

        even12 = ((self.Close2 - self.Open2) > 0) & (
            (abs(self.Close1 - self.Open1) * body).lt(self.Close2 - self.Open2)
        )
        even23 = ((self.Open - self.Close) > 0) & (
            (abs(self.Close1 - self.Open1) * body).lt(self.Open - self.Close)
        )
        even2 = np.where(
            self.Open1 < self.Close1,
            (self.High1 - self.Close1).between(
                (self.Open1 - self.Low1) * wick, (self.Open1 - self.Low1)
            ),
            (self.High1 - self.Open1).between(
                (self.Close1 - self.Low1) * wick, (self.Close1 - self.Low1)
            ),
        )
        even123 = (
            (self.High2.lt(self.High1))
            & (self.High1.gt(self.High))
            & even2
            & even12
            & even23
        )
        self.df["evening"] = np.where(even123, self.High, np.nan)

    def Hammers(self):

        cond1 = np.where(self.Open2 < self.Close2, self.Open2, self.Close2)
        cond2 = np.where(self.Open < self.Close, self.Open, self.Close)

        body = 2
        wick = 0.7

        ham12 = ((self.Open2 - self.Close2) > 0) & (
            (abs(self.Open1 - self.Close1) * body).lt(self.Open2 - self.Close2)
        )
        ham23 = ((self.Close - self.Open) > 0) & (
            (abs(self.Open1 - self.Close1) * body).lt(self.Close - self.Open)
        )
        ham2 = np.where(
            self.Open1 < self.Close1,
            self.Close1.between(self.High1 * wick, self.High1),
            self.Open1.between(self.High1 * wick, self.High1),
        ) & (abs(self.Open1 - self.Close1) * body < self.High1 - self.Low1)
        ham123 = (
            (self.Low2.gt(self.Low1))
            & (self.Low1.lt(self.Low))
            & np.where(
                self.Open1 < self.Close1,
                (self.Open1.lt(cond1)) & (self.Open1.lt(cond2)),
                (self.Close1.lt(cond1)) & (self.Close1.lt(cond2)),
            )
            & ham2
            & ham12
            & ham23
        )
        self.df["hammer"] = np.where(ham123, self.Low, np.nan)

        invham12 = ((self.Open2 - self.Close2) > 0) & (
            (abs(self.Open1 - self.Close1) * body).lt(self.Open2 - self.Close2)
        )
        invham23 = ((self.Close - self.Open) > 0) & (
            (abs(self.Open1 - self.Close1) * body).lt(self.Close - self.Open)
        )
        invham2 = np.where(
            self.Open1 < self.Close1,
            self.Open1.between(self.Low1 * wick, self.Low1),
            self.Close1.between(self.Low1 * wick, self.Low1),
        ) & (abs(self.Open1 - self.Close1) * body < self.High1 - self.Low1)
        invham123 = (
            (self.Low2.gt(self.Low1))
            & (self.Low1.lt(self.Low))
            & np.where(
                self.Open1 < self.Close1,
                (self.Open1.lt(cond1)) & (self.Open1.lt(cond2)),
                (self.Close1.lt(cond1)) & (self.Close1.lt(cond2)),
            )
            & invham2
            & invham12
            & invham23
        )
        self.df["invhammer"] = np.where(invham123, self.Low, np.nan)

        hang12 = ((self.Close2 - self.Open2) > 0) & (
            (abs(self.Close1 - self.Open1) * body).lt(self.Close2 - self.Open2)
        )
        hang23 = ((self.Open - self.Close) > 0) & (
            (abs(self.Close1 - self.Open1) * body).lt(self.Open - self.Close)
        )
        hang2 = np.where(
            self.Open1 < self.Close1,
            self.Close1.between(self.High1 * wick, self.High1),
            self.Open1.between(self.High1 * wick, self.High1),
        ) & (abs(self.Open1 - self.Close1) * body < self.High1 - self.Low1)
        hang123 = (
            (self.High2.lt(self.High1))
            & (self.High1.gt(self.High))
            & np.where(
                self.Open1 < self.Close1,
                (self.Close1.gt(cond1)) & (self.Close1.gt(cond2)),
                (self.Open1.gt(cond1)) & (self.Open1.gt(cond2)),
            )
            & hang2
            & hang12
            & hang23
        )
        self.df["hanging"] = np.where(hang123, self.High, np.nan)

        shoot12 = ((self.Close2 - self.Open2) > 0) & (
            (abs(self.Close1 - self.Open1) * body).lt(self.Close2 - self.Open2)
        )
        shoot23 = ((self.Open - self.Close) > 0) & (
            (abs(self.Close1 - self.Open1) * body).lt(self.Open - self.Close)
        )
        shoot2 = np.where(
            self.Open1 < self.Close1,
            self.Open1.between(self.Low1 * wick, self.Low1),
            self.Close1.between(self.Low1 * wick, self.Low1),
        ) & (abs(self.Open1 - self.Close1) * body < self.High1 - self.Low1)
        shoot123 = (
            (self.High2.lt(self.High1))
            & (self.High1.gt(self.High))
            & np.where(
                self.Open1 < self.Close1,
                (self.Close1.gt(cond1)) & (self.Close1.gt(cond2)),
                (self.Open1.gt(cond1)) & (self.Open1.gt(cond2)),
            )
            & shoot2
            & shoot12
            & shoot23
        )
        self.df["shooting"] = np.where(shoot123, self.High, np.nan)

    def RiseNFall(self):

        rise234 = (
            (self.Open3 > self.Close3)
            & (self.Open2 > self.Close2)
            & (self.Open1 > self.Close1)
            & (self.Open3 > self.Open2)
            & (self.Open2 > self.Open1)
        )
        rise1 = (
            (self.Close4 >= self.Open3)
            & (self.Open4 <= self.Close1)
            & (self.Close4 > self.Open4)
        )
        rise5 = (self.Close > self.Close4) & (self.Close > self.Open)
        rising = rise1 & rise234 & rise5
        self.df["rising"] = np.where(rising, self.Low, np.nan)

        fall234 = (
            (self.Open3 < self.Close3)
            & (self.Open2 < self.Close2)
            & (self.Open1 < self.Close1)
            & (self.Open3 < self.Open2)
            & (self.Open2 < self.Open1)
        )
        fall1 = (
            (self.Close4 <= self.Open3)
            & (self.Open4 >= self.Close1)
            & (self.Close4 < self.Open4)
        )
        fall5 = (self.Close < self.Close4) & (self.Close < self.Open)
        falling = fall1 & fall234 & fall5
        self.df["falling"] = np.where(falling, self.High, np.nan)

    def Engulfing(self):

        bullish = (
            (self.Open.lt(self.Close1))
            & (self.Close.gt(self.Open1))
            & (self.Open1 > self.Close1)
        )
        self.df["bullEngulf"] = np.where(bullish, self.Low, np.nan)

        bearish = (
            (self.Close.lt(self.Open1))
            & (self.Open.gt(self.Close1))
            & (self.Open1 < self.Close1)
        )
        self.df["bearEngulf"] = np.where(bearish, self.High, np.nan)

    def main(self):
        for i in self.candles:
            getattr(self, i)()
>>>>>>> v3
