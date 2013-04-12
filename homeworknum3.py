# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
# Python Imports
import csv
import datetime as dt
import math
# Third Party Imports
import matplotlib.pyplot as plt
from pylab import *
import pandas as pd
import numpy as np

# Initialize Trades List
trades = []

# Read order file
print "Reading signals2.csv"
with open ('orders.csv', 'rU') as infile:
    reader = csv.reader(infile, "excel")

    #read each line in order file
    for line in reader:
        trades.append([dt.datetime(int(line[0]), int(line[1]), int(line[2]), 16), line[3], line[4], int(line[5])])

# Prepare to read the data
trades = sorted(trades)
startday = trades[0][0]
endday = trades[-1][0]
timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(startday, endday, timeofday)
symbols = list(set([trade[1] for trade in trades]))


# Read close data from symbols list
print "Reading Data"
dataobj = da.DataAccess('Yahoo', cachestalltime=0)
close = dataobj.get_data(ldt_timestamps, symbols, 'close', verbose=True)
print "Finished Reading Data"

#
# Create Portfolio values based on trade information read in by CSV file indexed for timestamp

# Initialize Postions and Cash
position = close * 0
position['cash'] = float(0)

# Execute Trades and Calculate Portfolio Values

print "Executing Trades"
for trade in trades:
    symbol = trade[1]
    time = trade[0]
    qty = trade[3] if trade[2] == "Buy" else -trade[3]
    price = close[symbol][time]
    position[symbol][time] = position[symbol][time] + qty
    position['cash'][time] = position['cash'][time] - (qty * price)

for i in range(1, len(position.index)):
    position.ix[i] = position.ix[i] + position.ix[i - 1]

position['value'] = sum(position.ix[:, :-1] * close, axis=1) + position['cash'] + 1000000


with open('values3.txt', "w") as outfile:
    writer = csv.writer(outfile)

    for index in position.index:
        writer.writerow([index.year, index.month, index.day, position['value'][index], ""]) 
