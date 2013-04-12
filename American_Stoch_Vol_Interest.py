#
# Valuation of American Put Options
# Under Stochastic Volatility and Interest Rates
# Examples from Medvedev & Scaillet (2009):
# "Pricing American Options Under Stochastic Volatility
# and Stochastic Interest Rates"
# Working Paper No. 429, Finrisk --- MS (2009)
#
# (c) Visixion GmbH - Dr. Y. Hilpisch
# Script for illustration purposes only.
# August 2011
#
# SVSI_LSM_Con_Var.py
#
from numpy import *
from numpy . random import standard_normal , poisson , seed
from numpy . linalg import cholesky , lstsq
from datetime import *
from time import time
from SVSI_Euro_Valuation import *
t1 = time ()
d1 = datetime . now ()
# 'True' American Options Prices by Monte Carlo
# from MS (2009), table 3
trueList = array((( 0.0001 ,1.0438 ,9.9950 ,0.0346 ,1.7379 ,9.9823 ,
0.2040 ,2.3951 ,9.9726 ), # panel 1
(0.0619 , 2.1306 , 10.0386 ,0.5303 ,3.4173 , 10.4271 ,
1.1824 ,4.4249 , 11.0224 ) , # panel 2
(0.0592 , 2.1138 , 10.0372 ,0.4950 ,3.3478 , 10.3825 ,
1.0752 ,4.2732 , 10.8964 ) , # panel 3
(0.0787 , 2.1277 , 10.0198 ,0.6012 ,3.4089 , 10.2512 ,
1.2896 ,4.4103 , 10.6988 ))) # panel 4
# Cox, Ingersoll , Ross (1985) Parameters
# from MS (2009), table 3, panel 1
kappa_r =0.3
theta_r =0.04
sigma_r =0.1
r0 = 0.04
# Heston (1993) Parameters
# from MS (2009), table 3
para = array ((( 0.01 ,1.5 ,0.15 ,0.1 ), # panel 1
# (v0,kappa_v ,sigma_v ,rho)
(0.04, 0.75 ,0.3 ,0.1), # panel 2
(0.04 ,1.5 ,0.3 ,0.1 ), # panel 3
(0.04 ,1.5 ,0.15 ,-0.5 ))) # panel 4
theta_v = 0.02 # Long Term Volatility Level
S0 = 100.0 # Initial Index Level
# General Simulation Parameters
mL =[ 20 ] # Time Steps
iL =[ 35000 ] # Number of Paths per Valuation
tL =[ 1.0/12 , 0.25 ,0.5] # Maturity List
kL =[ 90 , 100 , 110 ] # Strike List
coVar =True # Use of Control Variates
moMatch =True # Random Number Correction (std + mean + drift)
antiPaths =False# Antithetic Paths for Variance Reduction
D= 10 # Number of Basis Functions
PY1 =0.025 # Performance Yardstick 1: Abs. Error in Currency Units
PY2 =0.015 # Performance Yardstick 2: Rel. Error in Decimals
R=5 # Number of Simulation Runs
SEED = 10000 # Seed Value
#
# Function for Short Rate and Volatility Processes
#
def eulerMRProc(x0 , sigma , kappa , theta , row , CM ):
    xh = zeros(( M +1, I), 'd')
    x= zeros (( M+1 ,I),'d')
    xh [0 ,:]= x0 ; x[0 ,:]= x0
    for t in range(1 ,M+1 ):
        ran = dot (CM , rand [: ,t ,:])
        xh [t ,:]+= xh [t -1 ,:]
        xh [t ,:]+= kappa *( theta - maximum (0 , xh [t -1 ,:]))* dt # Full Truncation
        xh [t ,:]+= sqrt ( maximum (0 , xh [t -1 ,:]))* sigma * ran [ row ]* sqrt ( dt )
        x[t ,:]= maximum (0 , xh [t ,:])
    return x
#
# Function for Heston Index Process
#
def eulerSExp(r ,S0 ,v , row , CM ):
    S = zeros((M+1, I),'d')
    S[0, :]= S0
    bias = 0.0
    for t in range(1 ,M+1 ,1 ):
        ran = dot (CM , rand [: ,t ,:])
        if moMatch ==True:
            bias = mean ( sqrt (v [t ,:])* ran [ row ]* sqrt ( dt ))
        S[t ,:]= S[t -1 ,:]* exp (((( r[t ,:]+ r [t -1 ,:])/ 2 -v[t ,:]/ 2 )* dt )+ sqrt (v[t ,:])* ran [ row ]* sqrt ( dt ) - bias )
    return S
    
def RNG(M ,I ):
    if antiPaths ==True:
        randDummy = standard_normal (( 3 ,M+1 , I/2 ))
        rand = concatenate (( randDummy ,- randDummy ) ,2)
    else:
        rand = standard_normal ((3 ,M +1 ,I ))
    if moMatch ==True:
        rand = rand / std ( rand )
        rand = rand - mean ( rand )
    return rand
#
# Valuation
#
t0 = time ()
for M in mL: # Number of Time Steps
    for I in iL: # Number of Paths
        t1 = time (); d1 = datetime . now ()
        absError =[]; relError =[]; l=0.0; errors = 0
# Name of the Simulation Setup
        name =('Base_'+str(R )+'_'+str(M )+'_'+str(I/ 1000 )+'_'
                +str( coVar )[ 0 ]+str( moMatch )[ 0 ]+str( antiPaths )[ 0 ]+
                '_'+str( PY1 * 100 )+'_'+str( PY2 * 100 ))
        seed ( SEED ) # RNG seed value
        for i in range( R ): # Simulation Runs
            print "\nSimulation Run %d of %d" %( i+1 ,R)
            print "----------------------------------------------------"
            print "Elapsed Time in Minutes %8.2f" %(( time () - t0 )/ 60 )
            print "----------------------------------------------------"
            for panel in range(4 ): # Panels
            # Correlation Matrix
                v0 , kappa_v , sigma_v , rho = para [ panel ,:]
                CovMat = zeros ((3 ,3 ),'d')
                CovMat [0 ,:]=[ 1.0 , rho , 0.0]
                CovMat [1 ,:]=[ rho ,1.0 , 0.0]
                CovMat [2 ,:]=[ 0.0 ,0.0 , 1.0]
                CM = cholesky ( CovMat )
                print "\n\n Results for Panel %d\n" %( panel +1)
                print " v0=%3.2f, sigma_v=%3.2f, kappa_v=%3.2f, rho=%3.2f" \
                    %( v0 , sigma_v , kappa_v , rho )
                print " ----------------------------------------------------"
                z=0
                for T in tL : # Times -to-Maturity
                    B0T =B ([ kappa_r , theta_r , sigma_r ,r0 , T ])
                    # Discount Factor B0(T)
                    r ,v ,S ,h ,V =0.0 , 0.0 , 0.0 ,0.0 ,0.0
                    # Memory Clean -up
                    dt =T/M
                    # Time Interval in Years
                    rand = RNG (M ,I )
                    # Random Numbers
                    r= eulerMRProc (r0 , sigma_r , kappa_r , theta_r ,0 , CM )
                    # Short Rate Process Paths
                    v= eulerMRProc (v0 , sigma_v , kappa_v , theta_v ,2 , CM )
                    # Volatility Process Paths
                    S= eulerSExp (r , S0 / S0 ,v ,1 , CM )
                    # Index Level Process Paths
                    print "\n Results for Time-to-Maturity %6.3f" %T
                    print " -----------------------------------------"
                    for K in kL : # Strikes
                        h ,V= 0.0 ,0.0 # Memory Clean -up
                        h= maximum (K/ S0 -S , 0) # Inner Value Matrix
                        V= maximum (K/ S0 -S , 0) # Value/Cash Flow Matrix
                        for t in range(M -1 ,0 ,-1 ):
                            df = exp ( -(( r [t ,:]+ r[t +1 ,:])/ 2 )* dt )
                            dummy = greater ( h[t ,:] , 0) # Select ITM Paths
                            relevant = nonzero ( dummy )
                            relS = compress ( dummy ,S [t ,:])
                            p=len( relS )
                            if p == 0:
                                cv = zeros (( I ),'d')
                            else:
                                relv = compress ( dummy ,v [t ,:])
                                relr = compress ( dummy ,r [t ,:])
                                relV =( compress ( dummy , V[t+1 ,:])* compress ( dummy , df ))
                                matrix = zeros (( D+1 ,p),'d')
                                matrix [ 10 ,:]= relS * relv * relr
                                matrix [9 ,:]= relS * relv
                                matrix [8 ,:]= relS * relr
                                matrix [7 ,:]= relv * relr
                                matrix [6 ,:]= relS ** 2
                                matrix [5 ,:]= relv ** 2
                                matrix [4 ,:]= relr ** 2
                                matrix [3 ,:]= relS
                                matrix [2 ,:]= relv
                                matrix [1 ,:]= relr
                                matrix [0 ,:]= 1
                                pol = lstsq ( matrix . transpose () , relV )
                                cv = dot ( pol [ 0], matrix )
                            erg = zeros (( I),'d')
                            put ( erg , relevant , cv )
                            V[t ,:]= where (h[t ,:] > erg ,h[t ,:] , V[t+1 ,:]* df )
                        df = exp ( -(( r [0 ,:]+ r[1 ,:])/ 2 )* dt )
                        ## European Option Values
                        C0 = H93_Value_Call_Int (S0 ,K ,T , B0T , kappa_v , theta_v , sigma_v , rho , v0 )
                        P0 = C0 + K* B0T - S0
                        P0_MCS = B0T *sum(h[ -1 ,:])/ I* S0
                        ## Determination of Correlation
                        x = B0T *h [-1 ,:]
                        y = V [1 ,:]* df
                        b = sum((x - mean (x ))*( y - mean ( y )))/sum((x - mean (x ))** 2 )
                        ## Control Variate Correction
                        if coVar ==True:
                            yCV =y -1.0 *( B0T * h[-1 ,:] - P0 / S0 )
                        # Set b instead of 1.0 to use stat. correlation
                        else:
                            yCV =y
                        SE = std ( yCV )/ sqrt (I )* S0
                        A0CV =max(sum( yCV )/ I*S0 ,h[0 ,0 ]) # LSM Control Variate
                        A0LS =max(sum(y )/ I*S0 , h[0 , 0 ]) # Pure LSM
                        ## Errors
                        diff = A0CV - trueList [ panel , z]
                        rdiff = diff / trueList [ panel ,z]
                        absError . append ( diff )
                        relError . append ( rdiff * 100 )
                        ## Output
                        br = " ----------------------------------"
                        print "\n Results for Strike %4.0f\n" %K
                        print " European Put Value MCS %8.4f" % P0_MCS
                        print " European Put Value Closed %8.4f" % P0
                        print " American Put Value LSM %8.4f" % A0LS
                        print " Correlation %8.4f" % b ,"\n",br
                        print " American Put Value CV %8.4f" % A0CV
                        print " Standard Error LSM CV %8.4f" % SE ,"\n",br
                        print " American Put Value Paper %8.4f" % trueList [ panel ,z ]
                        print " Valuation Error (abs) %8.4f" % diff
                        print " Valuation Error (rel) %8.4f" % rdiff
                        if abs( diff )< PY1 or abs( diff )/ trueList [ panel ,z]< PY2 :
                            print " Accuracy ok!\n"+ br
                            CORR =True
                        else:
                            print " Accuracy NOT ok!\n"+ br
                            CORR =False
                            errors = errors +1
                        print " %d Errors , %d Values , %.1f Min." \
                                %( errors ,len( absError ),float(( time () - t1 )/ 60 ))
                        print " %d Time Intervals , %d Paths" \
                                %(M ,I)
                        z=z +1;l =l+1
t2 = time (); d2 = datetime . now ()
br = "----------------------------------------------------"
print "\n\nOverall Statistics","\n"+ br
print "Start Calculations %32s\n" % str( d1 )+ br
print "Name of Simulation %32s" % name
print "Seed Value for RNG %32d" % SEED
print "Number of Runs %32d" % R
print "Time Steps %32d" % M
print "Paths %32d" % I
print "Control Variates %32s" % coVar
print "Moment Matching %32s" % moMatch
print "Antithetic Paths %32s\n" % antiPaths
print "Option Prices %32d" % l
print "Absolute Tolerance %32.4f" % PY1
print "Relative Tolerance %32.4f" % PY2
print "Errors %32d" % errors
print "Error Ratio %32.4f" % float( errors /l) +"\n"
print "Aver Val Error %32.4f" % (sum( array ( absError ))/ l )
print "Aver Abs Val Error %32.4f\n" % (sum(abs( array ( absError )))/ l)
print "Aver Rel Error %32.4f" % (sum( array ( relError ))/ l )
print "Aver Abs Rel Error %32.4f\n" % (sum(abs( array ( relError )))/ l)
print "Time in Seconds %32.4f" % ( t2 - t1 )
print "Time in Minutes %32.4f" % (( t2 - t1 )/ 60 )
print "Time per Option %32.4f" % float(( t2 - t1 )/ l )+"\n"+ br
print "End Calculations %32s" %str( d2 )+"\n"+ br