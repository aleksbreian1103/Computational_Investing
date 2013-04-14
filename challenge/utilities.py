__author__ = 'jjin'

from QSTK.qstkutil.qsdateutil import getNYSEdays
from QSTK.qstkutil.DataAccess import DataAccess
from QSTK.qstkutil.tsutil import returnize0

from datetime import timedelta
from copy import copy
import numpy as np
import pandas as pd
from itertools import chain


def fillNA(data):
    """
    fills the na in data
    @param data: a panda data frame
    """

    return data.fillna(method='ffill').fillna(method='bfill').fillna(1.0)


def getPrices(startDate, endDate, symbols, fields, fillna=True, isSymbolsList=False, includeLastDay=True):
    """
     reads stock prices from Yahoo
     the prices returned INCLUDE the endDate
     @param isSymbolsList: whether the symbols passed in is a stock symbol or a list symbol (e.g. sp5002012).
                           If true, symbols can contain only one symbol.
     @return prices with NaNs filled (forward, backward, 1.0)
    """

    assert not isSymbolsList or isinstance(symbols, str) or len(symbols) == 1, \
        'When isSymbolsList is true, symbols can only contain one symbol.'

    if includeLastDay:
        endDate += timedelta(days=1)

    dataReader = DataAccess('Yahoo')
    timeStamps = getNYSEdays(startDate, endDate, timedelta(hours=16))

    if isSymbolsList:
        symbols = dataReader.get_symbols_from_list(symbols if isinstance(symbols, str) else symbols[0])

    data = dataReader.get_data(timeStamps, symbols, fields)

    if fillna:
        data = fillNA(data)

#    data.index = pd.Series(data.index) - timedelta(hours=16)  # remove 16 from the dates

    return data


def calculateMetrics(prices, verbosity=2):
    """ Compute metrics of a series of prices
     @param prices: a series of prices. the dates are assumed consecutive and in increasing order
     @return stdDailyRets, avgDailyRets, sharpeRatio, cumRet
    """

    dailyReturns = copy(prices)
    returnize0(dailyReturns)

    stdDailyRets = np.std(dailyReturns)
    avgDailyRets = np.mean(dailyReturns)
    sharpeRatio = avgDailyRets / stdDailyRets * np.sqrt(252)
    cumRet = prices[-1] / prices[0]

    if verbosity >= 2:
        print '-------- Portfolio Prices ------------\n', prices
        print '\n-------- Portfolio Returns ------------\n', dailyReturns
    if verbosity >= 1:
        print '\n--------- Metrics -------------'
        print 'Final portfolio value =', prices[-1]
        print 'Date Range:', prices.index[0], 'to', prices.index[-1]
        print 'Sharpe Ratio =', sharpeRatio
        print 'Total return =', cumRet
        print 'Standard deviation of daily returns =', stdDailyRets
        print 'Average daily returns =', avgDailyRets

    return stdDailyRets, avgDailyRets, sharpeRatio, cumRet
   