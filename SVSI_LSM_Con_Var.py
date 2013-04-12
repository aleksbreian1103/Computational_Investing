# Least-Squares Monte Carlo for American Put Options
# with Antithetic Paths and Moment Matching

# Using In-The-Money Paths Only for Regression
# January 2013
#
from pylab import *
from time import time
import warnings
warnings.simplefilter('ignore', np.RankWarning)
t0 = time()
seed(10000)
 
#
# Parameters
#
# Option Parameters
s0 = [36., 38., 40., 42., 44.]  # Initial Index Levels
voL = [0.2, 0.4]  # Constant Volatilities
tL = [1.0, 2.0]    # Times-to-maturity
K = 40.    # Strike Price
r = 0.06   # Risk-Free Short Rate
 
# Simulation Parameters
M0 = 50    # Time Steps p.a.
I = 5000  # Simulation Paths
 
# Variance Reduction Techniques
antiPaths = True  # Antithetic Paths
moMatch = True   # Moment Matching
 
# Benchmark Values
bL = (4.478, 4.840, 7.101, 8.508,
      3.250, 3.745, 6.148, 7.670,
      2.314, 2.885, 5.312, 6.920,
      1.617, 2.212, 4.582, 6.248,
      1.110, 1.690, 3.948, 5.647)
 
#
# Random Numbers
#
def RNG(M, I):
    ''' Function to generate pseudo-random numbers with variance reduction.
    M: number of discrete time intervals
    I: number of simulated paths '''
    if antiPaths:
        ran = standard_normal((M, I / 2))
        rand = concatenate((ran, -ran), 1)  # Antithetic Variates
    else:
        rand = standard_normal((M, I))
    if moMatch:
        rand = rand - mean(rand)  # Matching of 1st Moment
        rand = rand / std(rand)  # Matching of 2nd Moment
    return rand
 
#

# LSM Algorithm
#

z = 0
for S0 in s0:
    for vol in voL:
        for T in tL:

            # Index Level Paths
 
            M = int(T * M0)    # Total Time Steps
            dt = T / M   # Length of Time Interval
            df = exp(-r * dt)  # Discount Factor
            rand = RNG(M, I)  # Random Numbers

            S = ones((M + 1, I), 'd')
            S[1:, :] = exp(cumsum((r - vol ** 2 / 2) * dt +
                                 vol * rand * sqrt(dt), axis=0))

            V = maximum(K - S * S0, 0)  # Value Array

            # Dynamic Optimization/Exercise Decisions
            for t in xrange(M - 1, 0, -1):
                ITM = V[t, :] > 0  # ITM or not
                relS = compress(ITM, S[t, :])  # Use only ITM-Paths
                relV = compress(ITM, V[t + 1, :] * df)
                regval = polyval(polyfit(relS, relV, 3), relS)  # Regression
                C = zeros(I, 'd')

                # Put Regression Values in New Array
                put(C, nonzero(ITM), regval)

                # Exercise Decision
                V[t, :] = where(V[t, :] > C, V[t, :], V[t + 1, :] * df)
            V0 = sum(V[1, :] * df) / I  # LSM Estimator

            # Output
            print ("S0 %3.0f | VOL %2.2f | T %2.0f | Value %6.3f |"
                 + " Benchmark %6.3f | Abs %6.3f | Rel %6.3f") \
                    % (S0, vol, T, V0, bL[z], V0 - bL[z],
                        (V0 - bL[z]) / bL[z] * 100)  # Output Values
            z += 1
print "Time in Seconds  %8.3f" % (time() - t0)
print "Time per Option  %8.3f" % ((time() - t0) / len(bL))
