#Rules
#1. Can pick each time once
#2. A loss is a strike
#3. 3 strikes and you're out

import os
import pandas as pd
import numpy as np

#df = pd.read_csv('nfl_games_2013.csv', index_col=['date'], parse_dates=['date'], infer_datetime_format=True)
df = pd.read_csv('nfl_games_2013.csv', parse_dates=['date'], infer_datetime_format=True)
playoff_mask = df['playoff'] == 0
df = df[playoff_mask]
first = df.date[0]
last = first + pd.offsets.Day(7)
df['Week'] = 0
mask = ((df['date'] >= first) & (df['date']<last))
#test = df[mask]
year = str(df.season[0])
#os.makedirs(year,exist_ok=True)
#print(test)
for i in range(17):
    mask = ((df['date'] >= first) & (df['date'] < last))
    df.Week[mask] = i+1
    #print(df[mask])
    #new_df=pd.DataFrame(test,)
    #test.to_csv((year+'/'+'Week ' + str(i+1) + '.csv'))
    first = last
    last = first + pd.offsets.Day(7)
#print(df.Week)
df['winner'] = df.team1
df['prob'] = abs(df.elo_prob1 - .5)
df.winner.where(df.result1 > 0 , other = df.team2, inplace = True)
#mask = Week_1.team1 == 'WSH'
#Week_1.team1[mask].index[0]
#is the same as
#Week_1.team1[Week_1.team1 == 'WSH'].index[0]
