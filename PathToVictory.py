# Rules
# 1. Can pick each time once
# 2. A loss is a strike
# 3. 3 strikes and you're out

import os
import pandas as pd
import numpy as np

# df = pd.read_csv('nfl_games_2013.csv', index_col=['date'], parse_dates=['date'], infer_datetime_format=True)
# df = pd.read_csv('nfl_games.csv', parse_dates=['date'], infer_datetime_format=True)
y = np.int64(2004)
while y < 2014:
    df = pd.read_csv('nfl_games.csv', parse_dates=['date'], infer_datetime_format=True)
    season_mask = (df['season'] == y)
    df = df[season_mask]
    playoff_mask = df['playoff'] == 0
    df = df[playoff_mask]
    first = df.date.iloc[0]
    last = first + pd.offsets.Day(7)
    df['Week'] = 0
    mask = ((df['date'] >= first) & (df['date'] < last))
    # test = df[mask]
    year = str(df.season.iloc[0])
    # os.makedirs(year,exist_ok=True)
    # print(test)
    for i in range(17):
        mask = ((df['date'] >= first) & (df['date'] < last))
        df.Week[mask] = i + 1
        # print(df[mask])
        # new_df=pd.DataFrame(test,)
        # test.to_csv((year+'/'+'Week ' + str(i+1) + '.csv'))
        first = last
        last = first + pd.offsets.Day(7)
    # print(df.Week)
    df['winner'] = df.team1
    df['prob'] = abs(df.elo_prob1 - .5)
    df.winner.where(df.result1 > 0, other=df.team2, inplace=True)
    # *** Oh here I go masking again ***#
    # mask = Week_1.team1 == 'WSH'
    # Week_1.team1[mask].index[0]
    # is the same as
    # Week_1.team1[Week_1.team1 == 'WSH'].index[0]
    # ## Find all possible solutions###
    # ##mask1.winner.sample(1).iloc[0]
    # #df[~df.winner.isin(picks)]
    # ##[df[df.Week == 1].winner.sample(1).iloc[0]]
    # #week_mask = df.Week == 1
    # ##df[['team1','elo_prob1']]
    # #and = & or = | not = ~
    upset_mask = ((df.result1 == 1.0) & (df.elo_prob1 < 0.5)) | ((df.result1 < 1.0) & (df.elo_prob1 > 0.5))
    upset_mask = ~upset_mask
    picks = []
    dfwins = pd.DataFrame(columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    prob_cutoff = .4
    while len(dfwins) < 1:
        prob_cutoff = round((prob_cutoff - .01), 5)
        t = 0
        prob_mask = df.prob >= prob_cutoff
        while t < 20000:
            picks = []
            dfpicks = pd.DataFrame(np.zeros(shape=(1, 17)),
                                   columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
            try:
                for i in range(17):
                    winner_mask = ~df.winner.isin(picks)
                    week_mask = df.Week == i + 1
                    randpick = df[winner_mask & week_mask & upset_mask & prob_mask].winner.sample(1).iloc[0]
                    # print(df[winner_mask & week_mask & upset_mask & prob_mask].prob)
                    picks.append(randpick)
                    dfpicks[i + 1].iloc[0] = randpick
                # print(dfpicks)
                dfwins = dfwins.append(dfpicks, ignore_index=True)
                # ##### Need to get them in rows of picks
                # print(dfwins)
            except:
                pass
                # print('no')
            t += 1
        print(prob_cutoff)
    # print(df[winner_mask & week_mask & upset_mask & prob_mask])
    print(dfwins)
    dfwins.drop_duplicates(inplace=True)
    dfwins.to_csv((str(y) + '_' + str(int((prob_cutoff + .5) * 100)) + '_' + str(t) + '.csv'))
    # print(picks)
    # multiloop weeks
    # picks = []
    # week_mask = df.Week == 1
    # permutation = 0
    # for i in range(len(df[winner_mask & (df.Week == 1) & upset_mask & prob_mask].winner)):
    #     pick_week1 = [df[winner_mask & (df.Week == 1) & upset_mask & prob_mask].winner.iloc[i]]

    # This doesnt work import itertools result = df.set_index(df['Week']) upset_mask = ((result.result1 == 1.0) & (
    # result.elo_prob1 < 0.5)) | ((result.result1 < 1.0) & (result.elo_prob1 > 0.5)) upset_mask = ~upset_mask
    # prob_cutoff = 0 prob_mask = result.prob >= prob_cutoff test = result[upset_mask& prob_mask] test2 = (list(
    # itertools.product(test.winner.loc[1].tolist(),test.winner.loc[2].tolist(),test.winner.loc[3].tolist( ),
    # test.winner.loc[4].tolist(),test.winner.loc[5].tolist(),test.winner.loc[6].tolist(), test.winner.loc[7].tolist(
    #  ),test.winner.loc[8].tolist(),test.winner.loc[9].tolist(), test.winner.loc[9].tolist(), test.winner.loc[
    # 10].tolist( ), test.winner.loc[11].tolist(), test.winner.loc[12].tolist(), test.winner.loc[13].tolist(),
    # test.winner.loc[ 14].tolist(), test.winner.loc[15].tolist(), test.winner.loc[16].tolist(), test.winner.loc[
    # 17].tolist(),)))
    y += 2
    print(y)

#
