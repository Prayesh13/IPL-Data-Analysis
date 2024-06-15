import pandas as pd
import numpy as np

matches = pd.read_csv("IPL_Matches.csv")
delivery = pd.read_csv("IPL_Ball_by_Ball.csv")

df = delivery.merge(matches,on='ID')
bowlingteam = df.apply(lambda row:row['Team2'] if(row['BattingTeam'] == row['Team1']) else row['Team1'],axis=1)
df.insert(16,'BowlingTeam',bowlingteam)

def rename_teams(cols):
    for i in cols:
        df[i].replace({'Rising Pune Supergiant': 'Rising Pune Supergiants',
                               'Kings XI Punjab': 'Punjab Kings',
                               'Delhi Daredevils': 'Delhi Capitals'}, inplace=True)

rename_teams(['BattingTeam','BowlingTeam','Team1','Team2','WinningTeam'])


df['Season'].replace({'2007/08' : '2008',
                     '2009/10' : '2010',
                     '2020/21' : '2020'},inplace=True)

def ipl_data():
    return df



def batsman_data(batsman):
    return df[df['Batter']==batsman]


def bowler_data(bowler):
    return df[df['Bowler'] == bowler]


def team_v_team(team1, team2):
    return df[((df['Team1'] == team1) & (df['Team2'] == team2)) |
            ((df['Team1'] == team2) & (df['Team2'] == team1))]

class Team():

    def teams(self):
        return sorted(df['Team1'].unique())



    def teamVsteam(self,team1,team2):
        team_df = team_v_team(team1,team2)
        tm = team_df['ID'].nunique()

        t1_win = team_df[team_df['WinningTeam'] == team1]['ID'].nunique()
        t2_win = team_df[team_df['WinningTeam'] == team2]['ID'].nunique()

        nr = tm - (t1_win + t2_win)

        response = {
            'Total Matches': str(tm),
            team1: t1_win,
            team2: t2_win,
            'No Result': nr
        }


        return response


    def plot_pie_team(self,response):
        d = pd.DataFrame([response])
        temp = pd.melt(d,var_name='Team',value_name='Result').iloc[1:,:]

        return temp

    def team_record(self,team):
        team_df = df[(df['Team1'] == team) | (df['Team2'] == team)]

        tm = team_df.ID.nunique()  # Total Matches Played by each team

        wins = team_df[team_df['WinningTeam'] == team].ID.nunique()  # Total Wins by each team

        loss = team_df[~(team_df['WinningTeam'] == team)].ID.nunique()  # Total Losses by each team

        no_result = tm - wins - loss

        titles = team_df[(team_df['MatchNumber'] == 'Final') & (team_df['WinningTeam'] == team)].ID.nunique()

        final_dict = {
            'Team' : team,
            'Total Matches' : tm,
            'Won' : wins,
            'Loss' : loss,
            'No Results' : no_result,
            'Title' : titles
        }

        return final_dict

    def team_wl_pie(self,team):
        response = self.team_record(team)
        return pd.DataFrame([response]).melt(var_name='Question', value_name='Answer').iloc[1:3, :]



class State:

    def func(self, x):
        return '-'.join(list(np.sort(x.values)))

    def parterships(self):
        df["batter-pair"] = df[["Batter", "NonStriker"]].apply(self.func, axis=1)

        temp = df.groupby("batter-pair").agg(
            {'TotalRun': 'sum', 'BatsmanRun': 'count', 'IsWicketDelivery': 'sum'}).reset_index()

        temp = temp.rename(columns={'TotalRun': 'Runs', 'BatsmanRun': 'Balls'})
        temp['StrikeRate'] = (temp['Runs'] / temp['Balls']) * 100
        temp['Average'] = (temp['Runs'] / temp['IsWicketDelivery'])
        temp['Batter1'] = temp['batter-pair'].str.split('-').str.get(0)
        temp['Batter2'] = temp['batter-pair'].str.split('-').str.get(1)
        ans = temp[['Batter1', 'Batter2', 'Runs', 'Balls', 'StrikeRate', 'Average']].sort_values(by='Runs',
                                                                                                   ascending=False).head(
            10)

        x = ans.set_index('Batter1').reset_index().reset_index()
        x['index'] = x['index'].shift(-1)
        x.loc[9, 'index'] = 10.0
        x['index'] = x['index'].astype('int')
        x.set_index('index', inplace=True)

        return x

    def fours(self):
        fours_df = df[df['BatsmanRun'] == 4]
        top_10_4 = fours_df.groupby('Batter')['BatsmanRun'].count().sort_values(ascending=False).head(10).reset_index()
        return top_10_4

    def sixes(self):
        six_df = df[df['BatsmanRun'] == 6]
        top_10_6 = six_df.groupby('Batter')['BatsmanRun'].count().sort_values(ascending=False).head(10).reset_index()
        return top_10_6

    def win_percentage(self):
        df = ipl_data()
        ipl1 = df[~(df['WinningTeam'].isna())]
        tm = ipl1['Team1'].value_counts() + ipl1['Team2'].value_counts()

        home_win = round((ipl1[ipl1['Team1'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
            'Team1'].value_counts() * 100, 2)
        away_win = round((ipl1[ipl1['Team2'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
            'Team2'].value_counts() * 100, 2)

        total_win = round((ipl1[ipl1['Team1'] == ipl1['WinningTeam']]['WinningTeam'].value_counts() +
                           ipl1[ipl1['Team2'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / tm * 100, 2)

        df = pd.DataFrame()
        df = df._append([tm.astype('int'), total_win, home_win, away_win], ignore_index=True)

        x = df.reset_index()
        x.loc[0, 'index'] = 'Total Matches'
        x.loc[1, 'index'] = 'Total Win(%)'
        x.loc[2, 'index'] = 'Home Win(%)'
        x.loc[3, 'index'] = 'Away Win(%)'

        return x.set_index('index')

class Points_table:
    def matches_played(self,data, team):
        return data[(data['Team1'] == team) | (data['Team2'] == team)].shape[0]

    def matches_won(self,data, team):
        return data[(data['WinningTeam'] == team)].shape[0]

    def matches_no_result(self,data, team):
        return data[((data['Team1'] == team) | (data['Team2'] == team)) & (data['WinningTeam'].isnull())].shape[0]
    def points_table(self, season):
        df = ipl_data()
        df = df[df['Season'] == season]
        temp = pd.DataFrame()
        temp['Team Name'] = df['Team1'].unique()
        temp['Matches Played'] = temp['Team Name'].apply(lambda x: self.matches_played(df, x))
        temp['Matches Won'] = temp['Team Name'].apply(lambda x: self.matches_won(df, x))
        temp['No Result'] = temp['Team Name'].apply(lambda x: self.matches_no_result(df, x))
        temp['Points'] = temp['Matches Won'] * 2 + temp['No Result']

        temp.sort_values(['Points', 'Matches Played'], ascending=False, inplace=True)
        temp.set_index('Team Name', inplace=True)

        return temp
