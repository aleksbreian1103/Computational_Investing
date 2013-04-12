# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 20:49:15 2013

@author: Aleks
"""
import pandas as pd
from pandas import Series
atemps = Series([101.5, 98, 0,85,100,92])
print atemps
print ""
sdtemps = atemps.drop(atemps.index[3])
print sdtemps
print ""
atemps.fillna(method = 'ffill')
print atemps
