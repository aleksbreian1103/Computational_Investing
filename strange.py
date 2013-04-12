__author__ = 'Aleks'
import pandas as pd

df_data = pd.read_csv("values3.csv", parse_dates=[[0,1,2]])

print df_data

df_data.values[0][1]