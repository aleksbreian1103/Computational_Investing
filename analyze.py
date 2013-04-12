
import datetime as dt
import pandas as pd
import csv
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
#import pandas.io.data as web

fundValue = []

print "Reading values3.txt"
with open ('values3.txt', 'rU') as infile:
    reader = csv.reader(infile, "excel")
    for row in reader:
        time = dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16, 0)
        fundValue.append(float(row[3]))

print time, fundValue
 
