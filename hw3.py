import csv
from datetime import date, datetime, timedelta
from collections import defaultdict
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import Portfolio as pf
import Equities as eq
import pandas as pd
import numpy as np
import QSTK.qstkutil.tsutil as tsu



def marketsim(cash, orders_file, data_item):
    # Read orders
    orders = defaultdict(list)
    symbols = set([])
    for year, month, day, sym, action, num in csv.reader(open(orders_file, "rU")):
        orders[date(int(year), int(month), int(day))].append((sym, action, int(num)))
        symbols.add(sym)
    
    days = orders.keys()
    days.sort()
    day, end = days[0], days[-1]
    
    # Reading the Data for the list of Symbols.
    timestamps = du.getNYSEdays(datetime(day.year,day.month,day.day),
                             datetime(end.year,end.month,end.day+1),
                             timedelta(hours=16))
    
    dataobj = da.DataAccess('Yahoo', cachestalltime = 0)
    close = dataobj.get_data(timestamps, symbols, data_item)
    
    values = []
    portfolio = pf.Portfolio(cash)
    for i, t in enumerate(timestamps):
        for sym, action, num in orders[date(t.year, t.month, t.day)]:
            if action == 'Sell': num *= -1
            portfolio.update(sym, num, close[sym][i])
        
        entry = (t.year, t.month, t.day, portfolio.value(close, i))
        values.append(entry)
        print values
    return values
    
#def computeportfoliostats(portfoliovalue):
#    totalvalue = np.array(portfoliovalue)
#    normalized_tvalue = totalvalue / totalvalue[0]
#    tsu.returnize0(normalized_tvalue)
#    mean = np.mean(normalized_tvalue)
#    volatility = np.std(normalized_tvalue)
#    sharpe = np.sqrt(252) * mean / volatility
#    return mean, volatility, sharpe;

def analyze(values):
    print eq.Equities([v[3] for v in values], "Portfolio")


if __name__ == "__main__":
    CASH = 1000000
    ORDERS_FILE = "ordersx.csv"
    BENCHMARK = "$SPX"
    
    analyze(marketsim(CASH, ORDERS_FILE, 'close'))
    
   # computeportfoliostats(s)    
   # print eq.Equities(BENCHMARK[1], "$SPX")