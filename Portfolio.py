from collections import defaultdict

class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.shares = defaultdict(int)
    
    def update(self, sym, num, share_cost):
        self.cash -= num * share_cost
        self.shares[sym] += num
    
    def value(self, close, d):
#        print self.cash + sum([num * close[sym][d] for sym, num in self.shares.iteritems()])
        return self.cash + sum([num * close[sym][d] for sym, num in self.shares.iteritems()])