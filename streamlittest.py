from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title("Test CSV import data website")
importArea = st.sidebar.file_uploader("Enter the CSV file here for analysis!", type=["csv"], accept_multiple_files=True)
for uploaded_file in importArea:
    if uploaded_file is not None:
        maindf = pd.read_csv(uploaded_file)
    st.write(maindf)
    maindf = maindf.drop_duplicates(subset=["Volunteer Name"], keep = 'last')
    volunteerSchool = maindf[['School']].copy()
    volunteerSchool = volunteerSchool[volunteerSchool["School"].str.contains("<NA>") == False]
    volunteerSchool['School Count'] = volunteerSchool.groupby('School')['School'].transform('size')
    volunteerSchool = volunteerSchool.drop_duplicates()
    volunteerSchool = volunteerSchool.sort_values('School Count', ascending=True).reset_index()
    st.write(volunteerSchool)
    schoolChart = px.data.gapminder()
    fig = px.bar(schoolChart, x='School', y='School Count')
    fig.show()
    st.bar_chart(volunteerSchool, x="School", y="School Count", width=2000, height=600)
    #testing
    #st.lmao