class EventStrategy:
    def __init__(self, order_file, threshold, num, hold_days):
        self.f = open(order_file, "w")
        self.threshold = threshold
        self.num = num
        self.hold_days = hold_days
        
    
    def add_order(self, timestamp, sym, action, num):
        self.f.write(",".join(map(str, [timestamp.year, timestamp.month, timestamp.day, sym, action, num])) + "\n")
    
    def threshold_event(self, eventmat, sym, prices, timestamps):
        for t in xrange(0, len(prices)):
            # The actual close of the stock price drops below a given threshold
            if prices[t-1] >= self.threshold and prices[t] < self.threshold:
                eventmat[sym][t] = 1.0
                self.add_order(timestamps[t               ], sym, "Buy" , self.num)
                self.add_order(timestamps[t+self.hold_days], sym, "Sell", self.num)
    
    def close(self):
        self.f.close()