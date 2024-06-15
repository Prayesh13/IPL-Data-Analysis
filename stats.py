import streamlit as st
from data import State


def stats_func():
    s = State()

    st.subheader("Good Batting Partners:")
    st.dataframe(s.parterships(), width=600, hide_index=True)

    st.write("-------------------------------------------------------")

    st.subheader("Home and Away Win Percentage's")
    st.dataframe(s.win_percentage())

    st.write("-------------------------------------------------------")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Most 4's : -")
        st.dataframe(s.fours(),width=500,hide_index=True)

    with col2:
        st.subheader("Most 6's : -")
        st.dataframe(s.sixes(),width=500,hide_index=True)


