import csv
from datetime import date, datetime, timedelta
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import datetime as dt
import pandas as pd
import numpy as np




dt_start = dt.datetime(2006, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

dataobj = da.DataAccess('Yahoo', cachestalltime=24)
ls_symbols = dataobj.get_symbols_from_list('sp5002012')
ls_symbols.append('SPY')
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)   
d_data = dict(zip(ls_keys, ldf_data))

for s_key in ls_keys:
    d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
    d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
    d_data[s_key] = d_data[s_key].fillna(1.0)

close_px_AAPL = d_data['close']['AAPL']
close_px_MSFT = d_data['close']['MSFT']
close_px_XOM = d_data['close']['XOM']
returns = d_data['close']/d_data['close'].shift(1) -1 

aapl_std250 = pd.rolling_std(close_px_AAPL, 250, min_periods = 10)
aapl_std250.plot()
corr = pd.rolling_corr(returns['AAPL'], returns['SPY'], 125, min_periods = 100)