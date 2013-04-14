import QSTK.qstkutil.qsdateutil as du
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

import QSTK.qstkutil.qsdateutil as du
if __name__ == '__main__':
    dt_timeofday = dt.timedelta(hours=16)
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    ls_symbols = ['GOOG']
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
     

    dataobj = da.DataAccess('Yahoo', cachestalltime=0)
   
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)   
    d_data = dict(zip(ls_keys, ldf_data))
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    #all_stocks = ldf_data #get_tickdata(ls_symbols=ls_symbols, ldt_timestamps=ldt_timestamps)
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