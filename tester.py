# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:22 2013

@author: Aleks
"""
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import time

temp = '/Users/Aleks/QSTK-0.2.5/QSTK/QSData/Yahoo/%s.csv'
path = temp % 'AAPL'

aapl_bars = pd.read_csv(temp % 'AAPL')
aapl_bars.index = pd.to_datetime(aapl_bars.pop('Date'))
aapl_bars.head()

def load_bars(ticker):
    bars = pd.read_csv(temp % ticker)
    bars.index = pd.to_datetime(bars.pop('Date'))
    return bars
    
aapl_bars.at_time(time(15, 0)).head(10) 
aapl_bars.Close['2009-10-15']   
mth_mean = aapl_bars.Close.resample('M', how=['mean', 'median', 'std'])
close = aapl_bars.Close
close / close.shift(1) - 1
minute_returns = aapl_bars.Close.pct_change()
std_10day = pd.rolling_std(minute_returns, 390 * 10)
std_10day.resample('B').plot()

import numpy as np
from pandas import DataFrame
dataFrame = DataFrame(np.arange(9).reshape((3,3)), index = ['this', 'is', 'now'], columns = ['a', 'b', 'c'])
dataFrame
dataFrame2 = dataFrame.reindex(['this', 'is', 'now', 'reindexed'])
dataFrame2