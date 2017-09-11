#Rules
#1. Can pick each time once
#2. A loss is a strike
#3. 3 strikes and you're out

import os
import pandas as pd
import numpy as np

df = pd.read_csv('nfl_games_2013.csv', parse_dates=['date'], infer_datetime_format=True)
first = df.ix[0,0]
last = first + pd.offsets.Day(7)
mask = ((df['date'] >= first) & (df['date']<last))
test = df[mask]
year = str(df.season[0])
os.makedirs(year,exist_ok=True)
print(test)
for i in range(17):
    mask = ((df['date'] >= first) & (df['date'] < last))
    test = df[mask]
    new_df=pd.DataFrame(test,)
    test.to_csv((year+'/'+'Week ' + str(i+1) + '.csv'))
    first = last
    last = first + pd.offsets.Day(7)