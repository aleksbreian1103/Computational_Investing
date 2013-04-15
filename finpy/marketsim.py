import sys
import csv
import matplotlib
matplotlib.use('Agg') # fix for matplotlib under multiprocessing
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import datetime as dt
import sets
from utils import get_tickdata
from equity import Equity
from portfolio import Portfolio
from order import Order

import QSTK.qstkutil.qsdateutil as du
if __name__ == '__main__':
    """
    python marketsim.py 1000000 orders.csv values.csv
    Where the number represents starting cash and orders.csv is a file of orders organized like this:
    2008, 12, 3, AAPL, BUY, 130
    2008, 12, 8, AAPL, SELL, 130
    2008, 12, 5, IBM, BUY, 50
    values.csv
    2008, 12, 3, 1000000
    2008, 12, 4, 1000010
    2008, 12, 5, 1000250
    """
    cash = 1000000
    order_file = 'orders.csv'
    value_file = 'values.csv'
    order_list = []
    dt_timeofday = dt.timedelta(hours=16)
    with open(order_file, 'rU') as csvfile:
        order_reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
        for row in order_reader:
            date = dt.datetime(int(row[0]),int(row[1]), int(row[2]), 16)
            o = Order(action=row[4], date=date, tick=row[3], shares=row[5])
            order_list.append(o)
    # order_list needs to be sorted. Otherwise the algorithm won't work.
    date_list = [x.date for x in order_list]
    date_list.sort()
    dt_start = date_list[0]     
    dt_end = date_list[-1] 
    tick_set = sets.Set([x.tick for x in order_list])
    ls_symbols = ['$SPX']
    while(tick_set):
        ls_symbols.append(tick_set.pop())
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    all_stocks = get_tickdata(ls_symbols=ls_symbols, ldt_timestamps=ldt_timestamps)
    pf = Portfolio(equities=all_stocks, cash=cash, dates=ldt_timestamps, order_list=order_list)
    pf.sim()
    equity_col = ['buy', 'sell', 'close']
    pf.csvwriter(csv_file=value_file, d=',', cash=False)
    print "Details of the Performance of the portfolio :"
    print "Data Range :",    ldt_timestamps[0],    "to",    ldt_timestamps[-1]
    print "Sharpe Ratio of Fund :", pf.sharpe() 
    print "Sharpe Ratio of $SPX :", pf.equities['$SPX'].sharpe()
    print "Total Return of Fund :", pf.totalrtn()
    print " Total Return of $SPX :", pf.equities['$SPX'].totalrtn()
    print "Standard Deviation of Fund :", pf.std()
    print " Standard Deviation of $SPX :", pf.equities['$SPX'].std()
    print "Average Daily Return of Fund :", pf.avg_dailyrtn()
    print "Average Daily Return of $SPX :", pf.equities['$SPX'].avg_dailyrtn()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pf.equities['$SPX'].plot(ax=ax, ldt_timestamps=ldt_timestamps, column='nml_price')
    pf.plot(ax=ax, ldt_timestamps=ldt_timestamps)
    legend = ['S&P 500', "Portfolio"]
    ax.legend(legend, loc=2)
    fig.autofmt_xdate()
    pdf_file = order_file + '.pdf'
    fig.savefig(pdf_file, format='pdf')
    
    import QSTK.qstkutil.qsdateutil as du
if __name__ == '__main__':
    dt_timeofday = dt.timedelta(hours=16)
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    ls_symbols = ['AAPL','GOOG', 'IBM', 'MSFT']
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    all_stocks = get_tickdata(ls_symbols=ls_symbols, ldt_timestamps=ldt_timestamps)
    mi = dict()
    up = dict()
    lo = dict()
    ba = dict()
    for sym in ls_symbols:
        mi[sym], up[sym], lo[sym], ba[sym] = all_stocks[sym].bollinger_band(tick=sym, k=1)
    for i in ldt_timestamps:
        outs = str(i)
        for s in ls_symbols:
            outs += "\t" + str(ba[s][i])
        print outs
