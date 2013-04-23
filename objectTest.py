# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 15:00:37 2013

@author: Aleks
"""

L = [1, -2, 3.4]

def applyToEach(L, f):
    for i in xrange(len(L)):
        L[i] = f(L[i])
        
applyToEach(L, abs)
print L        

applyToEach(L, int)
print L   

applyToEach(L, factorial)
print L 