import streamlit as st
from data import batsman_data,ipl_data
import plotly.express as px


# batsman Overall records :
def batter_overall_records(batsman):
    batsman_df = batsman_data(batsman)
    df = ipl_data()

    st.markdown(f"<h1 style='text-align: center; color:#54B4F3'>{batsman}</h1>", unsafe_allow_html=True)

    # batsman Total runs in ipl(2008-2023)
    runs = batsman_df['BatsmanRun'].sum()

    # Total number of balls palyed by the batsman in ipl(2008-2023)
    balls = batsman_df['BatsmanRun'].count()


    # Strike rate in ipl
    sr = (runs / balls) * 100

    # Number of fours smashed by the batsman
    fours = batsman_df[batsman_df['BatsmanRun'] == 4]['BatsmanRun'].count()

    # Number of fours smashed by the batsman
    sixes = batsman_df[batsman_df['BatsmanRun'] == 6]['BatsmanRun'].count()

    # Number of inning played by the batsman
    inn = batsman_df['ID'].nunique()

    # How many times batsman is out ?
    out = batsman_df[batsman_df['PlayerOut'] == batsman]['PlayerOut'].count()

    # Not Out
    notout = inn - out

    # Average in ipl
    avg = round(runs / out, 2)



    d = {
        'Runs': runs,
        'Strike Rate': sr,
        'Average': avg,
        'Innings Played': inn,
        'Out': out,
        'NotOut': notout,
        'Fours': fours,
        'Sixes': sixes
    }

    # represent in json format
    st.json(d)
    st.write("\n\n\n----------------------------")

    # season Graph that represent the batsman runs in each season
    st.write("Graph of Season wise batsman Runs ")
    season = season_wise(batsman_df)
    fig = px.bar(season, x='Season', y='BatsmanRun')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.write("\n\n\n----------------------------")

    # team Graph that represent the batsman run against each team
    st.write("Visual representation of the Batsman runs Against Each Teams")
    team_W = team_wise_record(batsman_df)
    fig1 = px.bar(team_W,x='BowlingTeam',y='BatsmanRun')
    st.plotly_chart(fig1, theme="streamlit",use_container_width=True)

    st.write("\n\n\n----------------------------")

    # Batsman Vs Bowler Pair (Big Rivalry in IPL)
    st.write("Batsman Vs Bowlers")
    st.dataframe(batsman_vs_bowlers(batsman_df))

    col1,col2 = st.columns(2)

    # Highest runs scored in ipl
    with col1:
        st.subheader("Highest Runs Scorer in IPL")
        st.dataframe(top_runs(df))


# season wise selected batsman runs :
def season_wise(batsman_df):
    return batsman_df.groupby('Season')['BatsmanRun'].sum().reset_index()


# Batsman run Vs Team
def team_wise_record(batsman_df):
    return batsman_df.groupby('BowlingTeam')['BatsmanRun'].sum().reset_index()

# Big Rivalry (Batsman vs Bowler)
def batsman_vs_bowlers(batsman_df):
    return (batsman_df.groupby('Bowler')[['BatsmanRun', 'IsWicketDelivery']].sum().sort_values(
        by=['BatsmanRun', 'IsWicketDelivery'], ascending=[False, False])
            .rename({'IsWicketDelivery' : 'Wickets'},axis=1).head(10))

# Highest runs scorer
def top_runs(df):
    return df.groupby(['Batter'])['BatsmanRun'].sum().sort_values(ascending=False).head(10)



