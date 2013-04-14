# Example of brownian simulation of correlated assets

#Import data
from pandas.io.data import DataReader
from pandas import Panel, DataFrame

symbols = ['AAPL', 'GLD', 'SPX', 'MCD']
data = dict((symbol, DataReader(symbol, "yahoo", pause=1)) for symbol in symbols)
panel = Panel(data).swapaxes('items', 'minor')
closing = panel['Close'].dropna()
closing.head()

# Calculate log returns
rets = log(closing / closing.shift(1)).dropna()
rets.head()

# Correlation Matrix
corr_matrix = rets.corr()
corr_matrix

# Plot correlation and scatter
from pandas.tools.plotting import scatter_matrix
scatter_matrix(rets);

#Cholesky decomposition
from scipy.linalg import cholesky
upper_cholesky = cholesky(corr_matrix, lower=False)
upper_cholesky

# Simulation parameters
# business days
import numpy as np 
from pandas import bdate_range   # business days

n_days = 21
dates = bdate_range(start=closing.ix[-1].name, periods=n_days)
n_assets = len(symbols)
n_sims = 50000
dt = 1./252
mu = rets.mean().values
sigma = rets.std().values * np.sqrt(252)
# Generate correlated random values
          # init random number generator for reproducibility
rand_values = np.random.standard_t(df = 20, size = (n_days * n_sims, n_assets)) #
corr_values = rand_values.dot(upper_cholesky)*sigma

# Run simulation
prices = Panel(items=range(n_sims), minor_axis=symbols, major_axis=dates)
prices.ix[:, 0, :] = closing.ix[-1].values.repeat(n_sims).reshape(4,n_sims).T # set initial values
for i in xrange(1,n_days):
    prices.ix[:, i, :] = prices.ix[:, i-1,:] * (np.exp((mu-0.5*sigma**2)*dt +  np.sqrt(dt)*corr_values[i::n_days])).T    

prices.ix[123, :, :].head()   # show random path

# Plot results
prices.ix[::10, :, 'AAPL'].plot(title='AAPL', legend=False);

# Statistics for last day
print(prices.ix[:, -1, :].T.describe())



