import pandas_ta as ta

class Indicators():
    def __init__(self,df,indicators):
        self.df = df
        self.indicators = indicators
        self.addindi()
        
    def addindi(self):
        for indi in self.indicators.keys():
            if self.indicators[indi]:
                for i in self.indicators[indi]:
                    kwargs = i
                    getattr(self.df.ta,indi.lower())(**kwargs)
            else:
                getattr(self.df.ta,indi.lower())(append=True)