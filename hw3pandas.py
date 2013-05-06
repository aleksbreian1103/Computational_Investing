
"""
hw3 using just pandas
Created on Sun May  5 19:43:46 2013

@author: Aleks
"""
import argparse as ap
from pandas import *
import pandas as pd
import numpy as np
import math
import copy
import csv
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu


argparser = ap.ArgumentParser()
argparser.add_argument("cash",type=float)
argparser.add_argument("infile")
argparser.add_argument("outfile")

args = argparser.parse_args()

#can't parse dates at this point due to duplicates, empty column deals with last comma
df = pd.read_csv(args.infile,
names=['year','month','day','symbol','order_type','qty','empty'], header=None )

#creates a separate column for dates due to duplicates
df['dates'] = df.apply(lambda row: dt.datetime(row['year'],row['month'],row['day'],16), axis=1)

#drop unneeded date fields
df = df.drop(['year','month','day','empty'],axis=1)

#create a condition to deal with Sell orders
cond = df['order_type'] == 'Sell'

#if row contains sell, change quantity to negative
df.qty[cond] = df.qty[cond]*-1 

#pivot the table to have datetime index and stocks as columns
df_pivot = pivot_table(df,values='qty',rows=['dates'],cols=['symbol'],aggfunc={'qty':'sum'})

df_pivot = df_pivot.fillna(0)

#get close prices
startdate = min(df['dates'])
enddate = max(df['dates'])


timeofday = dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startdate,enddate,timeofday)

symbols = list(set(df['symbol']))

dataobj = da.DataAccess('Yahoo')
close = dataobj.get_data(timestamps, symbols, "close")

df_pivot = df_pivot.reindex(close.index)
#df_pivot = df_pivot.fillna(0)

totalOrders = (df_pivot*close).sum(axis=1)*-1
totalOrders[0]=totalOrders[0]+args.cash
totalOrders = totalOrders.fillna(0)
cash = totalOrders.cumsum()

df_pivot = df_pivot.fillna(0)
df_pivot = df_pivot.cumsum(axis=0)

#new_df = df_pivot * close

portfolio = df_pivot * close


#print portfolio.sum(axis=1).head(20)
totalPortfolio = cash + portfolio.sum(axis=1)

print totalPortfolio.head(20)
totalPortfolio.to_csv('values.csv')
