import pandas as pd
import numpy as np
from batter import batter_overall_records
from bowler import bowler_overall_records
from Team_analysis import team_app
from stats import stats_func
from points_table import pt

import streamlit as st
from streamlit_option_menu import option_menu

# import the data :
matches = pd.read_csv("IPL_Matches.csv")
delivery = pd.read_csv("IPL_Ball_by_Ball.csv")

df = delivery.merge(matches,on='ID')
bowlingteam = df.apply(lambda row:row['Team2'] if(row['BattingTeam'] == row['Team1']) else row['Team2'],axis=1)
df.insert(16,'BowlingTeam',bowlingteam)

st.set_page_config(page_title='IPL Analysis', layout = 'wide', initial_sidebar_state = 'auto')

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 500px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)

with st.sidebar:
    main_option = option_menu(
        menu_title='IPL Analysis',
        options=["Team Analysis", 'Batter', 'Bowler','Stats','Points Table'],
        menu_icon='point',
        styles={
            "container": {"padding": "10!important", "background-color": 'black'},
            "icon": {"color": "white", "font-size": "13px"},
            "nav-link": {"color": "white", "font-size": "13px", "text-align": "left", "margin": "0px",
                         "--hover-color": "blue"},
            "nav-link-selected": {"background-color": "#02ab21"}, }

    )

# Team analysis
if main_option == 'Team Analysis':
    team_app()


# Batter Analysis
elif main_option == 'Batter':
    st.title("Batsman Analysis")
    batter_name = st.sidebar.selectbox("Select the batsman : ",sorted(delivery.Batter.unique()))
    btn = st.sidebar.button("show")

    if btn:
        batter_overall_records(batter_name)

# IPL Famous Stats
elif main_option == 'Stats':
    st.title("IPL Stats : ")
    stats_func()


# Points Table
elif main_option == 'Points Table':
    pt()


# Bowler Analysis
else:
    st.title("Bowling Analysis")
    bowler_name = st.sidebar.selectbox("Select the Bowler : ", sorted(delivery['Bowler'].unique()))
    btn = st.sidebar.button("show")

    if btn:
        bowler_overall_records(bowler_name)

