# I loath QSTK
import QSTK.qstkutil.DataAccess as da   
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd



startday = dt.datetime(2010,5,1)
endday = dt.datetime(2010,6,25)
stock='AAPL'
symbols = [stock]
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

dataobj = da.DataAccess('Yahoo', cachestalltime = 0)
adjclose = dataobj.get_data(timestamps, symbols, "close")

adjclose = adjclose.fillna(method ='ffill')
adjclose = adjclose.fillna(method='backfill')

# Get the 20 day moving avg and moving stddev
movavg = pd.rolling_mean(adjclose,20,min_periods=20)
movstddev = pd.rolling_std(adjclose, 20, min_periods=20)

# Compute the upper and lower bollinger bands
#Bollinger_val = (price - rolling_mean) / (rolling_std) 
upperband = (movstddev + movavg) / movstddev
lowerband = (movstddev - movavg) / movstddev
bollingerVal = (adjclose - movavg) / movstddev
# Plot the adjclose, movingavg, upper and lower bollinger bands
plt.clf()

plt.plot(adjclose.index,bollingerVal.values)
#plt.plot(adjclose.index,movavg[stock].values/100)
plt.plot(adjclose.index,upperband[stock].values)
plt.plot(adjclose.index,lowerband[stock].values)
plt.xlim(adjclose.index[10], adjclose.index[len(adjclose.index)-1])

plt.legend(['MSFT','Moving Avg.','Upper Bollinger Band','Lower Bollinger Band'],
           loc='upper left')
plt.ylabel('Adjusted Close')
plt.xlabel('Date')
savefig("bollinger1.pdf", format='pdf')

# Normalize the upper and lower bollinger bands in range [-1,+1]
normalizedupperband = upperband - movavg  + 1
normalizedlowerband = lowerband - movavg  - 1

# Normalize the Bollinger %b indicator in the range [-1,+1]
#normalizedindicator = 1*(adjclose - movavg)/movstddev

# plot the normalized bollinger upper band, lower band and indicator
plt.clf()
plt.plot(adjclose.index,bollingerVal.values)
plt.plot(adjclose.index,normalizedupperband[stock].values)
plt.plot(adjclose.index,lowerband[stock].values)
plt.axhline(y=1, color='gray')
plt.axhline(y=-1, color='gray')
plt.xlim(adjclose.index[0], adjclose.index[len(adjclose.index)-1])

#plt.legend(['Normalized Indicator','Normalized Upper Bollinger Band','Normalized Lower Bollinger Band'], loc='upper left')
plt.ylabel('Bollinger Feature')
plt.xlabel('Date')
savefig("bollinger2.pdf", format='pdf')