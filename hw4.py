"""
Use the actual close $5.00 event with the 2012 SP500 data.

I expect that this strategy should make money.
Use the following parameters:
  * Starting cash: $50,000
  * Start date: 1 January 2008
  * End date: 31 December 2009
  * When an event occurs, buy 100 shares of the equity on that day.
  * Sell automatically 5 trading days later.

Compute the Sharpe Ratio, total return and STDDEV of daily returns.
"""
from datetime import datetime

def marketsim(cash, orders_file, data_item):
    # Read orders
    orders = defaultdict(list)
    symbols = set([])
    for year, month, day, sym, action, num in csv.reader(open(orders_file, "rU")):
        orders[date(int(year), int(month), int(day))].append((sym, action, int(num)))
        symbols.add(sym)
    
    days = orders.keys()
    days.sort()
    day, end = days[0], days[-1]
    
    # Reading the Data for the list of Symbols.
    timestamps = du.getNYSEdays(datetime(day.year,day.month,day.day),
                             datetime(end.year,end.month,end.day+1),
                             timedelta(hours=16))
    
    dataobj = da.DataAccess('Yahoo')
    close = dataobj.get_data(ldt_timestamps, symbols, data_item)
    
    values = []
    portfolio = Portfolio(cash)
    for i, t in enumerate(timestamps):
        for sym, action, num in orders[date(t.year, t.month, t.day)]:
            if action == 'Sell': num *= -1
            portfolio.update(sym, num, close[sym][i])
        
        entry = (t.year, t.month, t.day, portfolio.value(close, i))
        values.append(entry)
    
    return values
    
class Equities:
    def __init__(self, values, name=None):
        self.values = values
        self.name = name
        self.returns = map(self.single_return, range(1, len(self.values)))
    
    def roi(self, start, end):
        if self.values[end] == self.values[start]: return 0
        return (self.values[end] / self.values[start]) - 1
    
    def tot_return(self):
        return self.roi(0, -1)
    
    def single_return(self, d):
        return self.roi(d-1, d)
    
    def average_return(self):
        return mean(self.returns)
    
    def stdev_return(self):
        return std(self.returns)
    
    def sharpe_ratio(self):
        return (self.average_return() / self.stdev_return()) * sqrt(len(self.values))
    
    def __str__(self):
        return '\n'.join([
            "\n[%s]" % (self.name if self.name is not None else "Equities"),
            "Sharpe Ratio     : %.6f" % self.sharpe_ratio(),
            "Total Return     : %.4f" % self.tot_return(),
            "Average Daily Ret: %.6f" % self.average_return(),
            "STDEV Daily Ret  : %.6f" % self.stdev_return(),
        ])    
# analyze
def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            #f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            #f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            #f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            #f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol is down more then x% while
            if f_symprice_yest >= 9.0 and f_symprice_today < 9.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events
        
def analyze(values):
    print Equities([v[3] for v in values], "Portfolio")
    


class EventStrategy:
    def __init__(self, order_file, threshold, num, hold_days):
        self.f = open(order_file, "w")
        self.threshold = threshold
        self.num = num
        self.hold_days = hold_days
        
    
    def add_order(self, timestamp, sym, action, num):
        self.f.write(",".join(map(str, [
            timestamp.year, timestamp.month, timestamp.day,
            sym, action, num
        ])) + "\n")
    
    def threshold_event(self, eventmat, sym, prices, timestamps):
        for t in range(1, len(prices)):
            # The actual close of the stock price drops below a given threshold
            if prices[t-1] >= self.threshold and prices[t] < self.threshold:
                eventmat[sym][t] = 1.0
                self.add_order(timestamps[t               ], sym, "Buy" , self.num)
                self.add_order(timestamps[t+self.hold_days], sym, "Sell", self.num)
    
    def close(self):
        self.f.close()


if __name__ == "__main__":
    START_DAY = datetime(2008,  1,  1)
    END_DAY   = datetime(2009, 12, 31)
    SYMBOLS_STOCK_YEAR = 2012
    THRESHOLD = 7
    CASH = 100000
    ORDERS_FILE = "orders_event.csv"
    BUY_N = 100
    HOLD_DAYS = 5
    CLOSE_TYPE = "actual_close"

    
    strategy = EventStrategy(ORDERS_FILE, THRESHOLD, BUY_N, HOLD_DAYS)
    strategy.close()
    analyze(marketsim(CASH, ORDERS_FILE, "close"))