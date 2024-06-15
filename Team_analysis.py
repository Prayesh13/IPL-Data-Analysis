import streamlit as st
import plotly.express as px
from data import Team


def team_app():

    obj = Team()

    # select team1
    team1 = st.sidebar.selectbox("Select Team 1 -",obj.teams())

    # select team2
    team2 = st.sidebar.selectbox("Select Team 2 -", obj.teams())

    btn = st.sidebar.button("Show")

    # Team1 Vs Team2 Status
    team_rec = obj.teamVsteam(team1,team2)

    if btn:
        st.title("Team Analysis")
        st.markdown(f"<h3 style='text-align: center; color:#FF3380'>{team1}</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color:#FFFFFF'>Vs</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color:#FF3380'>{team2}</h3>", unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Head to Head:')
            st.dataframe(team_rec, column_config={'': 'Question', 'value': 'Answer'}, width=500)


        st.write("\n\n-----------------\n\n\n")
        st.subheader("Pie Chart of the Wining Percentages")

        chart = obj.plot_pie_team(team_rec)


        fig = px.pie(chart, names='Team', values='Result', hover_name='Team', labels='Team')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True, width=400, height=400)
        st.plotly_chart(fig,theme='streamlit',use_container_width=True)

        st.write("\n\n-----------------\n\n\n")
        st.write("Team Records ")
        col3,col4 = st.columns(2)

        with col3:
            team1_rec = obj.team_record(team1)
            st.dataframe(team1_rec, column_config={'': 'Question', 'value': 'Answer'}, width=500)
            fig = px.pie(obj.team_wl_pie(team1), names='Question', values='Answer', hover_name='Question', labels='Question')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=True, width=400, height=400)
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

        with col4:
            team2_rec = obj.team_record(team2)
            st.dataframe(team2_rec, column_config={'': 'Question', 'value': 'Answer'}, width=500)
            fig = px.pie(obj.team_wl_pie(team2), names='Question', values='Answer', hover_name='Question',
                         labels='Question')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=True, width=400, height=400)
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)


