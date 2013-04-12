import csv
from datetime import date, datetime, timedelta
from collections import defaultdict
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import pandas as pd
import QSTK.qstkutil.tsutil as tsu
from pandas import DataFrame
from pandas import Series
import numpy as np

# Path to file, and read file into DataFram
fileName = '/Users/Aleks/QSTK-0.2.5/QSTK/QSData/Yahoo/$SPX.csv'
newFrame = pd.read_table(fileName, sep=',')
#newFrame.sort_index(ascending=False, axis = 0)
closing = newFrame.Close[175:415]
closing = closing.sort_index(ascending=False)
frame1 = DataFrame(closing)
#normalized = frame1.values/frame1.values[0]
#normalized
#returns = normalized.copy()
#tsu.returnize0(returns)
#returns
#average(returns)
#sum(returns)
#std(returns)

na_close = frame1.Close.values
ls_allocations = [1.0]
# Create Analyse Function


def analyse(na_close, ls_allocations):

    # Normalize the close price
    na_norm_close = na_close / na_close[-1]

    # Get weighted daily returns
    weighted_daily_close = na_norm_close

    # Copy the weighted daily close to a new ndarray to find returns
    port_daily_ret = weighted_daily_close.copy()

    # Calculate daily returns of the portfolio close price
    tsu.returnize0(port_daily_ret)

    # Get average portfolio daily returns
    daily_ret = np.average(port_daily_ret)

    # Calculate volatility of average weighted daily returns
    vol = np.std(port_daily_ret)

    # Calculate Sharpe Ratio
    k = np.math.sqrt(252)
    sharpe = k * (daily_ret/vol)

    # Calculate Cumulative Return
    cum_ret = (na_close[-1]/na_close[0])

    return vol, daily_ret, sharpe, cum_ret
    
vol, daily_ret, sharpe, cum_ret = analyse(na_close, ls_allocations)  
