from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import geopy as gp
import geopandas as gpd
import pgeocode
from geopy.geocoders import Nominatim
from datetime import datetime
#locator = Nominatim(user_agent="testing", timeout=20)
nomi = pgeocode.Nominatim('us')
st.title("HIM Event Data Breakdown")
st.write("This app uses the Google Sheets event data of volunteers to provide analysis on HIM and its impacts on parts of the Bay Area compared to others.")
st.write("Below is a quick tutorial on how to obtain the CSV file necessary for the data breakdown!")
st.write("First, you'll need to navigate to the event you'd like to get the data for in your Google Drive.")
st.write("Make sure that you are logged into your _first_\._last_\@heartinmotion.org email to access all the event spreadsheets.")
st.write("Next, follow the steps in this image to download the spreadsheet as a CSV file! Make sure you are downloading the Master tab.")
st.image("oaklandtutorial.png")
st.write("Now, click on the browse button on the sidebar to the left of this and locate your downloaded CSV file.")
st.image("oaklandbrowse.png")
st.write("That's it! Now the data you've imported has been visualized in graphs and maps for you.")
st.write("_Note: This app has not been tested with a wide variety of event spreadsheets and errors may occur. You can email me at rishabh.mahesh@heartinmotion.org or reach out to me on WorkChat(Rishabh Mahesh) if you have any questions, concerns, or feedback._")
importArea = st.sidebar.file_uploader("Enter the CSV file here for analysis!", type=["csv"], accept_multiple_files=True)
for uploaded_file in importArea:
    if uploaded_file is not None:
        maindf = pd.read_csv(uploaded_file)
        st.balloons()
    st.header("Event Dataset")
    st.write(maindf)
    maindf = maindf.drop_duplicates(subset=["Volunteer Name"], keep = 'last')
    volunteerSchool = maindf[['School']].copy()
    volunteerSchool = volunteerSchool[volunteerSchool["School"].str.contains("<NA>") == False]
    volunteerSchool['School Count'] = volunteerSchool.groupby('School')['School'].transform('size')
    volunteerSchool = volunteerSchool.drop_duplicates()
    volunteerSchool = volunteerSchool.sort_values('School Count', ascending=True).reset_index()
    #schoolChart = px.data.gapminder()
    #fig = px.bar(schoolChart, x='School', y='School Count')
    #fig.show()
    st.header("School Distribution of Event Volunteers")
    st.bar_chart(volunteerSchool, x="School", y="School Count", width=2000, height=600)
    #
    #def location_info(x ='San Francisco School of the Art'):
    #    data = locator.geocode(x).raw #use this line when using Nominatim
    #    data_converted = pd.json_normalize(data).squeeze() #squeeze converts a dataframe to a pandas series
    #
    #    return data_converted
    #y = location_info()
    #volunteerSchool = volunteerSchool["School"].apply(location_info)
    #st.write(volunteerSchool)
    #st.write(y)
    maindf = maindf[maindf["School"].str.contains("<NA>") == False]
    maindf = maindf.drop_duplicates()

    zipDf = maindf[['Zip code']].copy().dropna()
    zipLatList = []
    zipLongList = []
    for index, row in zipDf.iterrows():
        
        #data = {
        #    "lat": query["latitude"],
        #    "lon": query["longitude"]
        #}
        #st.write(int(row["Zip code"]))
        query = nomi.query_postal_code(int(row["Zip code"]))
        zipLatList.append(query["latitude"])
        zipLongList.append(query["longitude"])
    #st.write(zipList)
    st.header("Location Distribution of Event Volunteers")
    zipData = pd.DataFrame({'latitude':zipLatList, 'longitude':zipLongList})
    st.map(zipData)
    st.write("_None of this data is based off of addresses, but rather zip codes, so personal information is kept safe._")
    seniorCount = 0
    juniorCount = 0
    sophomoreCount = 0
    freshmanCount = 0
    eightCount = 0
    sevenCount = 0 
    miscCount = 0
    for index, row in maindf.iterrows():
        if (datetime.now().month) >=6 :
            if(int(row["Year"]) - datetime.now().year) == 1:
                #print("Senior")
                seniorCount = seniorCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 2:
                #print("Junior")
                juniorCount = juniorCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 3:
                #print("Sophomore")
                sophomoreCount = sophomoreCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 4:
                #print("Freshman")
                freshmanCount = freshmanCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 5:
                #print("8th grade")
                eightCount = eightCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 6:
                #print("7th grade")
                sevenCount = sevenCount + 1
            if(int(row["Year"]) - datetime.now().year ) > 6:
                #print("Misc")
                miscCount = miscCount + 1
        else:
            if(int(row["Year"]) - datetime.now().year) == 0:
                #print("Senior")
                seniorCount = seniorCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 1:
                #print("Junior")
                juniorCount = juniorCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 2:
                #print("Sophomore")
                sophomoreCount = sophomoreCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 3:
                #print("Freshman")
                freshmanCount = freshmanCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 4:
                #print("8th grade")
                eightCount = eightCount + 1
            if(int(row["Year"]) - datetime.now().year ) == 5:
                #print("7th grade")
                sevenCount = sevenCount + 1
            if(int(row["Year"]) - datetime.now().year ) > 6:
                #print("Misc")
                miscCount = miscCount + 1
    gradeDistDf = pd.DataFrame({"Seniors":[seniorCount], "Juniors": [juniorCount], "Sophomores":[sophomoreCount], "Freshmen": [freshmanCount], "8th graders": [eightCount], "7th graders": [sevenCount], "Miscellaneous": [miscCount]})
    gradeDistDfT = gradeDistDf.transpose().reset_index()
    gradeDistDfT.columns = ['Grade', 'Count']

    # Define the chart
    bars = alt.Chart(gradeDistDfT).mark_bar().encode(
        x='Count:Q',
        y=alt.Y('Grade:O', sort=['Seniors', 'Juniors', 'Sophomores', 'Freshmen', '8th graders', '7th graders', 'Miscellaneous']),
        color='Grade:N'
    ).properties(
    width=1000,
    height=500)

    # Add labels to the bars
    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3
    ).encode(text='Count:Q')

    # Combine the chart and labels
    st.header("Grade Distribution of Event Volunteers")
    chart = (bars + text).properties(
        title=''
    ).configure_axis(labelFontSize=16, titleFontSize=18).configure_title(fontSize=24)
    st.altair_chart(chart)
    