import csv
from collections import defaultdict
import copy
from numpy import NAN
import datetime as dt
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil
import QSTK.qstkstudy.EventProfiler as ep

class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.shares = defaultdict(int)
    
    def update(self, sym, num, share_cost):
        self.cash -= num * share_cost
        self.shares[sym] += num
    
    def value(self, close, d):
        return self.cash + sum([num * close[sym][d] for sym, num in self.shares.iteritems()])


def marketsim(cash, orders_file, data_item):
    # Read orders
    orders = defaultdict(list)
    symbols = set([])
    for year, month, day, sym, action, num in csv.reader(open(orders_file, "rU")):
        orders[dt.date(int(year), int(month), int(day))].append((sym, action, int(num)))
        symbols.add(sym)
    
    days = orders.keys()
    days.sort()
    day, end = days[0], days[-1]
    
    # Reading the Data for the list of Symbols.
    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
    dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    close = dataobj.get_data(ldt_timestamps, symbols, data_item)
    
    values = []
    portfolio = Portfolio(cash)
    for i, t in enumerate(ldt_timestamps):
        for sym, action, num in orders[dt.date(t.year, t.month, t.day)]:
            if action == 'Sell': num *= -1
            portfolio.update(sym, num, close[sym][i])
        
        entry = (t.year, t.month, t.day, portfolio.value(close, i))
        values.append(entry)
    
    return values

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
        
def analyze(values):
    print Equities([v[3] for v in values], "Portfolio")



CASH = 1000000
ORDERS_FILE = "orders.csv"
BENCHMARK = "$SPX"
    
analyze(marketsim(CASH, ORDERS_FILE, "close"))