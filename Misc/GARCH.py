"""
Naive GARCH implementation
Naive in the sense that alpha and beta (or q and p) are drawn from a uniform
distribution rather than estimated with MLE
"""

import numpy                                                                                                                                                                                                                                                                                                                                  
from pandas.io.data import DataReader
from pandas import Panel
import numpy as np 
symbols = ['AAPL', 'GLD', 'SPX', 'MCD']
data = dict((symbol, DataReader(symbol, "yahoo", pause=1)) for symbol in symbols)
panel = Panel(data).swapaxes('items', 'minor')
closing = panel['Close'].dropna()
closing_two = closing[:-1]
# Calculate log returns
rets = log(closing / closing.shift(1)).dropna()
rets_tn = log(closing_two / closing_two.shift(1)).dropna()



sigma = rets.std().values * np.sqrt(252)
sigma_tn = rets_tn.std().values * np.sqrt(252)

u_tn = rets['AAPL'][-2]

#######################
## Naive GARCH(1, 1) ##
#######################
# General form: sigma^2(t) = gamma*Vl + alpha*u(n-1)^2 + beta*sigma(n-1)^2
# General variance forecast: E[sigma^2(n+k)] = Vl + (alpha + beta)^k * (sigma(n)^2 - Vl)

sigma_tn = sigma_tn[0]
#omega = gamma * Vl
gamma_param = 0
while True:
    alpha = numpy.random.uniform(0,1) 
    beta = numpy.random.uniform(0,1) 
    if alpha + beta < 1.0:
        gamma_param = 1 - alpha - beta
        break
    else:
        print("Parameters unstable")
        break   

f1 = alpha * u_tn**2
f2 = beta * sigma_tn**2
Vl = (sigma[0]**2 - f1 - f2)/gamma_param

k = 5

E_Variance_k = Vl + (alpha + beta)**k * (sigma[0]**2 - Vl)

#Forecasted Variance
print(E_Variance_k)    
print("")                                                                                                                                                                      
print("")
print("")
                
#### Not Done ###                                                                                                                                                              
#def historical_bootstrap(rets):                                                                                                                                        
#    mean = sum(rets) / float(len(rets))                                                                                                                         
#    udd = []                                                                                                                                                                  
#    returns_ignored, sigma_hat = garch(len(rets))                                                                                                                      
#    for r_d, sigma_hat_d in zip(rets, sigma_hat):                                                                                                                      
#        udd_d = (r_d - mean) / sigma_hat_d                                                                                                                                    
#        udd.append(udd_d)                                                                                                                                                     
#    return udd                                                                                                                                                                
#                                                                                                                                                                              
#                                                                                                                                                                              
#if __name__ == "__main__":                                                                                                                                                    
#    #print garch(10)                                                                                                                                                           
#    print historical_bootstrap(rets['AAPL'])  