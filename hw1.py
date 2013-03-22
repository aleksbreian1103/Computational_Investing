import datetime as dt
import pandas
import numpy
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil
import QSTK.qstkstudy.EventProfiler


class Equities:
    def __init__(self, values, name=None):
        self.values = values
        self.name = name
        self.returns = map(self.single_return, range(1, len(self.values)))
    
    def roi(self, start, end):
        if self.values[end] == self.values[start]: return 0
        return (self.values[end] / self.values[start]) - 1
    
    def tot_return(self):
        return self.roi(0, -1)
    
    def single_return(self, d):
        return self.roi(d-1, d)
    
    def average_return(self):
        return mean(self.returns)
    
    def stdev_return(self):
        return std(self.returns)
    
    def sharpe_ratio(self):
        return (self.average_return() / self.stdev_return()) * sqrt(len(self.values))
    
    def __str__(self):
        return '\n'.join([
            "\n[%s]" % (self.name if self.name is not None else "Equities"),
            "Sharpe Ratio     : %.6f" % self.sharpe_ratio(),
            "Total Return     : %.4f" % self.tot_return(),
            "Average Daily Ret: %.6f" % self.average_return(),
            "STDEV Daily Ret  : %.6f" % self.stdev_return(),
        ])


if __name__ == '__main__':
    # TODO: sharp ratio higher than 4?
    PORTFOLIO = (
        ('AAPL' , 0.6),
        ('GLD'  , 0.2),
        ('WMT'  , 0.1),
        ('CVX'  , 0.1)
    )
    
    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)
    dt_timeofday = dt.timedelta(hours=16)
    
    # Get only the days when the US market is open:
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
    
    BENCHMARK = 'SPY'
    symbols = [s for s, _ in PORTFOLIO] + [BENCHMARK]
    
    close = da.DataAccess('Yahoo').get_data(ldt_timestamps, symbols, "close")
    
    print Equities([sum([close[s][i] for s in symbols]) for i in range(len(ldt_timestamps))], "Portfolio")
    print Equities([     close[BENCHMARK][i]            for i in range(len(ldt_timestamps))], "Benchmark")