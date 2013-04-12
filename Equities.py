import numpy as np

class Equities:
    def __init__(self, values, name=None):
        self.values = values
        self.name = name
        self.returns = map(self.single_return, xrange(0, len(self.values)))
    
    def roi(self, start, end):
        if self.values[end] == self.values[start]: return 0
        return (self.values[end] / self.values[start]) - 1
    
    def tot_return(self):
        return self.roi(0, -1)+1
    
    def single_return(self, d):
        if d == 0:
            return 0
        else:    
            return self.roi(d-1, d)
    
    def average_return(self):
        return np.mean(self.returns)
    
    def stdev_return(self):
        return np.std(self.returns)
    
    def sharpe_ratio(self):
        return (self.average_return() / self.stdev_return()) * np.sqrt(252)
    
    def __str__(self):
        return '\n'.join([
            "\n[%s]" % (self.name if self.name is not None else "Equities"),
            "Sharpe Ratio     : %.15f" % self.sharpe_ratio(),
            "Total Return     : %.15f" % self.tot_return(),
            "Average Daily Ret: %.15f" % self.average_return(),
            "STDEV Daily Ret  : %.15f" % self.stdev_return(),])