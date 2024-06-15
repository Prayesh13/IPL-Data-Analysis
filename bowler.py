from data import bowler_data,ipl_data
import plotly.express as px
import streamlit as st

def bowler_overall_records(bowler):

    st.markdown(f"<h1 style='text-align: center; color:#80E956'>{bowler}</h1>", unsafe_allow_html=True)
    bowler_df = bowler_data(bowler)


    col1,col2 = st.columns(2)
    l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
         'hit wicket']
    x = bowler_df[bowler_df['Kind'].isin(l)]

    with col1:
        st.subheader("Total Wickets")
        st.subheader(str(x['IsWicketDelivery'].sum()))

    with col2:
        st.subheader("Best Bowling Performance : ")
        temp_df = bowler_df[(~bowler_df['ExtraType'].isin(['legbyes','byes']))]
        temp_df_f = temp_df[(~temp_df['Kind'].isin(['run out']))]

        st.dataframe(temp_df_f.groupby(['ID','BattingTeam'])[['TotalRun','IsWicketDelivery']].sum()
                     .sort_values(by=['IsWicketDelivery','TotalRun'],
                        ascending=[False,True]).head(1).reset_index().drop(columns='ID').set_index('BattingTeam'))

    st.write("Season wise Analysis ")
    st.plotly_chart(season_wise_record(x), theme="streamlit",use_container_width=True)

    st.write("Team wise Analysis ")
    st.plotly_chart(team_wise_records(x), theme="streamlit", use_container_width=True)

    st.write("\n\n\n----------------------------")

    col3,col4 = st.columns(2)
    ipl = ipl_data()
    df = ipl[ipl['Kind'].isin(l)]

    with col3:
        st.subheader("Top 10 Highest Wicket Tacker in IPL Till 2023")

        st.dataframe(df.groupby('Bowler')['IsWicketDelivery'].sum().sort_values(ascending=False).head(10).reset_index().rename(
            {'IsWicketDelivery': 'Wickets'}, axis=1),hide_index=True)

    with col4:

        st.subheader("Top-10 Battles in IPL till 2023")
        temp_df = df[~(df['Kind'].isin(['run out', 'retired hurt', 'retired out', 'obstructing the field']))]
        st.dataframe(temp_df.groupby(['Batter', 'Bowler'])[['BatsmanRun', 'IsWicketDelivery']].sum().reset_index().sort_values(
            by=['IsWicketDelivery', 'BatsmanRun'], ascending=[False, True]).head(10),hide_index=True)

    st.write("\n\n\n----------------------------")
    st.subheader("IPL Purple cap holder in Each Season")
    st.dataframe(purple_cap(df),hide_index=True,width=400,height=600)


def season_wise_record(x):
    # x = bowler_df[bowler_df['Kind'].isin(l)]
    df_b = x.groupby('Season')['IsWicketDelivery'].sum().reset_index().rename({'IsWicketDelivery' : 'Wickets'},axis=1)
    fig1 = px.bar(df_b, x='Season', y='Wickets')
    return fig1



def team_wise_records(x):
    df_b = x.groupby('BattingTeam')['IsWicketDelivery'].sum().reset_index().rename({'IsWicketDelivery': 'Wickets'}, axis=1)
    fig1 = px.bar(df_b, x='BattingTeam', y='Wickets')
    return fig1


def purple_cap(x):
    return (x.groupby(['Season', 'Bowler'])['IsWicketDelivery'].sum().reset_index().
            rename({'IsWicketDelivery': 'Wickets'},axis=1).sort_values(by=['Season', 'Wickets'],
            ascending=[True, False]).drop_duplicates(subset=['Season']))
