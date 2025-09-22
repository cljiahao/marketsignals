import numpy as np

class SupNRes():
    def __init__(self,df,SNR):
        self.df = df
        self.SNR = SNR if len(SNR) != 0 else ["WinShift15"]
        self.main()
    
    def levels(self):
        with open('levels.txt',"r") as f:
            levels = f.read().split('\n')
            self.levels = []
            for i in levels:
                self.levels.append([0,float(i.split(',')[-1][1:-1])])        

    # to make sure the new level area does not exist already
    def SNRMean(self,value):    
        avg =  np.mean(self.df['High'] - self.df['Low'])   
        return np.sum([abs(value-level)<avg for _,level in self.levels])==0

    def WinShift(self,dur):
        self.levels = []
        dur = int(dur)
        max, min = [], []
        for i in range(dur, len(self.df)-dur):
            # WinShift for High Range (Resistance)
            high_range = self.df['High'][i-dur:i+dur-1]
            current_max = high_range.max()
            if current_max not in max:
                max = []
            max.append(current_max)
            if len(max) == dur and self.SNRMean(current_max):
                self.levels.append((high_range.idxmax(), current_max))

            # WinShift for Low Range (Support)
            low_range = self.df['Low'][i-dur:i+dur]
            current_min = low_range.min()
            if current_min not in min:
                min = []
            min.append(current_min)
            if len(min) == dur and self.SNRMean(current_min):
                self.levels.append((low_range.idxmin(), current_min))

        with open('levels.txt','w') as f:
            f.write('\n'.join(str(item) for item in self.levels))

    def Fractal(self):
        # determine bullish fractal
        def is_support(i):  
            cond1 = self.df['Low'][i] < self.df['Low'][i-1]   
            cond2 = self.df['Low'][i] < self.df['Low'][i+1]   
            cond3 = self.df['Low'][i+1] < self.df['Low'][i+2]   
            cond4 = self.df['Low'][i-1] < self.df['Low'][i-2]  
            return (cond1 and cond2 and cond3 and cond4) 

        # determine bearish fractal
        def is_resistance(i):  
            cond1 = self.df['High'][i] > self.df['High'][i-1]   
            cond2 = self.df['High'][i] > self.df['High'][i+1]   
            cond3 = self.df['High'][i+1] > self.df['High'][i+2]   
            cond4 = self.df['High'][i-1] > self.df['High'][i-2]  
            return (cond1 and cond2 and cond3 and cond4)

        self.levels = []
        for i in range(2,self.df.shape[0]-2):
            if is_support(i):
                sup = self.df['Low'][i]
                if self.SNRMean(sup):
                    self.levels.append((i,sup))
            elif is_resistance(i):
                res = self.df['High'][i]
                if self.SNRMean(res):
                    self.levels.append((i,res))
                    
    def main(self):
        for i in self.SNR:
            if i[:8] == "WinShift":
                getattr(self,i[:8])(i[8:])
            else:
                getattr(self,i)()
