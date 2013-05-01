from collections import defaultdict
import csv
import copy
from numpy import nan as NA
from pandas import DataFrame
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import Equities as eq
import Portfolio as pf
"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['close']
    ts_market = df_close['SPY']

    print "Finding Events"
    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index
    
    #df_close = DataFrame(df_close)

    movavg = pd.rolling_mean(df_close, 20, min_periods = 20)
    movstddev = pd.rolling_std(df_close, 20, min_periods=20)

    bollingerVal = (df_close - movavg) / movstddev
    
    bollingerValY = copy.deepcopy(bollingerVal)
    bollingerValSPY= copy.deepcopy(bollingerVal)
       
    for s_sym in ls_symbols:
        for i in xrange(1, len(ldt_timestamps)):
            #bollingerVal = df_close[s_sym].ix[ldt_timestamps[i]]
            #bollingerValY = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            #f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            #f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
         
            if bollingerVal[s_sym].ix[ldt_timestamps[i]] <=-2.0 and bollingerValY[s_sym].ix[ldt_timestamps[i - 1]] >= -2.0 and bollingerValSPY ['SPY'].ix[ldt_timestamps[i]] >= 1.4:
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo', cachestalltime = 24)
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1)

    df_events = find_events(ls_symbols, d_data)
    print "Creating Study"
    

    
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
                
    def marketsim(cash, orders_file, data_item, dataobj):
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
        timestamps = du.getNYSEdays(dt.datetime(day.year,day.month,day.day),
                             dt.datetime(end.year,end.month,end.day+1),
                             dt.timedelta(hours=16))
    
#    dataobj = da.DataAccess('Yahoo', cachestalltime = 0)
        close = dataobj.get_data(timestamps, symbols, data_item)
    
        values = []
        portfolio = pf.Portfolio(cash)
        for i, t in enumerate(timestamps):
            for sym, action, num in orders[dt.date(t.year, t.month, t.day)]:
                if action == 'Sell': num *= -1
                portfolio.update(sym, num, close[sym][i])
        
        entry = (t.year, t.month, t.day, portfolio.value(close, i))
        values.append(entry)
        
        return values     


    def analyze(values):
        print eq.Equities([v[3] for v in values], "Portfolio")
        
    CASH = 100000
    ORDERS_FILE = "orders_event.csv"
    BUY_N = 100
    HOLD_DAYS = 5
    CLOSE_TYPE = "actual_close"
    
    analyze(marketsim(CASH, ORDERS_FILE, "close", dataobj))


       
