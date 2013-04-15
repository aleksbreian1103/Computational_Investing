"""
(c) 2013 Tsung-Han Yang
This source code is released under the New BSD license.  
blacksburg98@yahoo.com
Created on April 1, 2013
"""
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import QSTK.qstkutil.qsdateutil as du
import utils as ut

class Equity(pd.DataFrame):
    """
    Equity is something that will be/was/is in the Portfolio.
    buy is either a NaN, or a floating number. 
    If buy is a floating number, then we buy the number of shares of the equity.
    sell is either a NaN, or a floating number.
    shares is the daily balance of the equities.
    """
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False, init_share=0.0):
        if columns == None:
            cols = ['open', 'high', 'low', 'close', 'volume', 'actual_close', 'nml_close', 'buy',
            'sell', 'shares']
        else:
            cols = columns
        pd.DataFrame.__init__(self, data=data, index=index, columns=cols, dtype=dtype, copy=copy)
        self['shares'][0] = init_share
        self['buy'] = 0.0
        self['sell'] = 0.0

    def buy(self, date, shares, price, ldt_timestamps):
        self.fillna_shares(date, ldt_timestamps)
        self['buy'][date] = shares
        self['shares'][date] += shares

    def sell(self, date, shares, price, ldt_timestamps):
        self.fillna_shares(date, ldt_timestamps)
        self['sell'][date] = shares
        self['shares'][date] -= shares
        return price*shares

    def fillna_shares(self, date, ldt_timestamps):
        last_valid = self['shares'].last_valid_index()
        self['shares'][last_valid:date] = self['shares'][last_valid]

    def nml_close(self):
        self['nml_close'] = self['close']/self['close'].ix[0]
        return self['nml_close']

    def plot(self, ax, ldt_timestamps, column):
        ax.plot(ldt_timestamps, self[column])

    def dailyrtn(self):
        """
        Return the return of each day, a list.
        """
        daily_rtn = []
        ldt_timestamps = self['close'].index
        for date in range(len(ldt_timestamps)):
            if date == 0:
                daily_rtn.append(0)
            else:
             daily_rtn.append((self['close'][date]/self['close'][date-1])-1)
        return daily_rtn

    def avg_dailyrtn(self): 
        return np.average(self.dailyrtn())

    def std(self):
        return np.std(self.dailyrtn())

    def sharpe(self, k=252):
        return np.sqrt(k) * self.avg_dailyrtn()/self.std()

    def totalrtn(self):
        return self['close'][-1]/self['close'][0]

    def moving_average(self, tick, window=20, nml=False):
        """
        Return an array of moving average. Window specified how many days in
        a window.
        """
        mi = self.bollinger_band(tick=tick, window=window, nml=nml, mi_only=True)
        return mi

    def bollinger_band(self, tick, window=20, k=2, nml=False, mi_only=False):
        """
        Return four arrays for Bollinger Band.
        The first one is the moving average.
        The second one is the upper band.
        The thrid one is the lower band.
        The fourth one is the Bollinger value.
        If mi_only, then return the moving average only.
        """
        ldt_timestamps = self.index
        dt_timeofday = dt.timedelta(hours=16)
        days_delta = dt.timedelta(days=(np.ceil(window*7/5)+5))
        dt_start = ldt_timestamps[0] - days_delta
        dt_end = ldt_timestamps[0] - dt.timedelta(days=1)
        pre_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
        # ldf_data has the data prior to our current interest.
        # This is used to calculate moving average for the first window.
        ldf_data = ut.get_tickdata([tick], pre_timestamps)
        if nml:
            ma_data = pd.concat([ldf_data[tick]['nml_close'], self['nml_close']]) 
        else:
            ma_data = pd.concat([ldf_data[tick]['close'], self['close']])
        bo = dict()
        bo['mi'] = pd.rolling_mean(ma_data, window=window)[ldt_timestamps] 
        if mi_only:
            return bo['mi']
        else:
            sigma = pd.rolling_std(ma_data, window=window)
            bo['up'] = bo['mi'] + k * sigma[ldt_timestamps] 
            bo['lo'] = bo['mi'] - k * sigma[ldt_timestamps] 
            bo['ba'] = (ma_data[ldt_timestamps] - bo['mi']) / (k * sigma[ldt_timestamps])
            return bo

    def beta_alpha(self, market):
        """
        market is a Equity representing the market. 
        It can be S&P 500 or Russel 2000.
        """
        beta, alpha = np.polyfit(market["close"], self["close"], 1)
        return beta, alpha

