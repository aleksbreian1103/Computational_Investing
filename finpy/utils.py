"""
(c) 2013 Tsung-Han Yang
This source code is released under the New BSD license.  
blacksburg98@yahoo.com
Created on April 1, 2013
"""
from collections import defaultdict
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du




import QSTK.qstkutil.tsutil as tsu
import dataaccess as da
import equity as Equity

def get_tickdata(ls_symbols, ldt_timestamps):
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_symbols, ldf_data))
    for s_key in ls_symbols:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    stocks = dict()
    for s in ls_symbols:
        stocks[s] = Equity(index=ldt_timestamps, data=d_data[s])
        stocks[s].nml_close()
    return stocks 

