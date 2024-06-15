from data import Points_table
import streamlit as st
from data import ipl_data

df = ipl_data()
df['Season'] = df['Season'].str.strip().astype(int)
def pt():
    p = Points_table()

    season = st.sidebar.selectbox("Select Season",sorted(list(df['Season'].unique())))
    btn = st.sidebar.button("Show")

    if btn:
        st.title(f"Points Table of Season : {season}")
        st.dataframe(p.points_table(season), width=700)