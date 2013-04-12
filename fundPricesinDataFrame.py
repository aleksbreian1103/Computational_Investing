import datetime as dt
import pandas as pd
import csv
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da


time = []
fund = []

print "Reading values3.txt"
with open('values3.csv', 'rU') as infile:
    reader = csv.reader(infile, "excel")
    for row in reader:
        print row
        time.append(dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16))
        fund.append(row[3])
        #fundValue.append([time, close])
        #print time, fund

fund_close = pd.DataFrame(fund, index=time, columns=['fund'])
print fund_close + '\n'
