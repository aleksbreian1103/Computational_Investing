import csv
import copy
from numpy import NAN
import datetime as dt
from datetime import date, timedelta
from collections import defaultdict
import QSTK.qstkutil.DataAccess as da   
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkstudy.EventProfiler as ep
import QSTK.qstkutil.tsutil as tsu
from pandas import DataFrame
from pandas import Series
import pandas as pd
import numpy as np
import Portfolio as pf
import Equities as eq
import EventStrategy as es

def fetchData():
    dataobj = da.DataAccess('Yahoo', cachestalltime = 0)
    return dataobj

def marketsim(cash, orders_file, data_item, dataobj):
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
    timestamps = du.getNYSEdays(dt.datetime(day.year,day.month,day.day),
                             dt.datetime(end.year,end.month,end.day+1),
                             timedelta(hours=16))
    
#    dataobj = da.DataAccess('Yahoo', cachestalltime = 0)
    close = dataobj.get_data(timestamps, symbols, data_item)
    
    values = []
    portfolio = pf.Portfolio(cash)
    for i, t in enumerate(timestamps):
        for sym, action, num in orders[date(t.year, t.month, t.day)]:
            if action == 'Sell': num *= -1
            portfolio.update(sym, num, close[sym][i])
        
        entry = (t.year, t.month, t.day, portfolio.value(close, i))
        values.append(entry)
        
    return values
    

        
def analyze(values):
    print eq.Equities([v[3] for v in values], "Portfolio")


def findEvents(symbols_year, startday, endday, event, data_item, dataobj):
#    dataobj = da.DataAccess('Yahoo', cachestalltime = 0)
    symbols = dataobj.get_symbols_from_list("sp500%d" % symbols_year)
    symbols.append('SPY')
    
    # Reading the Data for the list of Symbols.
    timestamps = du.getNYSEdays(startday, endday, timedelta(hours=16))
    
    # Reading the Data
    print "# reading data"
    close = dataobj.get_data(timestamps, symbols, data_item)
#    print close
    # Generating the Event Matrix
    print "# finding events"
    eventmat = copy.deepcopy(close)
    for sym in symbols:
        for time in timestamps:
            eventmat[sym][time] = NAN
    
    for symbol in symbols:
        event(eventmat, symbol, close[symbol], timestamps)
    
    return eventmat

    for sym in ls_symbols:
      if np.nansum(df_events[sym].values) > 0:
        pdf = sym + ".pdf"
        png = sym + ".png"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(ldt_timestamps, d_data['actual_close'][sym])
        for i in range(len(df_events[sym].values)):
          if df_events[sym].values[i] == 1:
            ax.axvline(x=ldt_timestamps[i], visible=True, c='r')
        ax.legend(['actual close'], loc=2)
        fig.autofmt_xdate()
#        plt.savefig(pdf, format='pdf')
        plt.savefig(png, format='png')

if __name__ == "__main__":
    START_DAY = dt.datetime(2008,  1,  1)
    END_DAY   = dt.datetime(2009, 12, 31)
    SYMBOLS_STOCK_YEAR = 2012
    THRESHOLD = 9
    CASH = 50000
    ORDERS_FILE = "orders_event.csv"
    BUY_N = 100
    HOLD_DAYS = 5
    CLOSE_TYPE = "actual_close"
    
    dataobj = fetchData()
    strategy = es.EventStrategy(ORDERS_FILE, THRESHOLD, BUY_N, HOLD_DAYS)
    findEvents(SYMBOLS_STOCK_YEAR, START_DAY, END_DAY,
               strategy.threshold_event, 'actual_close', dataobj)
    strategy.close()
    
    analyze(marketsim(CASH, ORDERS_FILE, "close", dataobj))
