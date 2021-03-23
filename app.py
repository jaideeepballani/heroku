import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px

st.title("NAS Daily Course Dashboard")
#st.header("Data Visualization Board for Winery Inc Chemical Components")
df = pd.read_csv("./Customer Info_NasAcademy.csv")

n_tz = df['timezone'].nunique()
top_k_tz = st.sidebar.slider('Choose the Number of Top Earning Timezones', 0, n_tz+1, (0, n_tz+1), 1)[1]
st.subheader("Most Profitable Timezones")
tmp = df.groupby('timezone')['fullAmount'].apply(sum)
by_timezone = pd.DataFrame({'timezone':tmp.index, 'totalAmount':tmp}).sort_values(['totalAmount'], ascending = False).reset_index(drop=True)
st.dataframe(by_timezone.head(top_k_tz))

n_course = df['courseOfferId'].nunique()
top_k_courses = st.sidebar.slider('Choose the Number of Top Earning Courses', 0, n_course+1, (0, n_course+1), 1)[1]
#top_k_courses = n_course if top_k_courses > n_course else top_k_courses
st.subheader("Most Profitable Courses")
tmp = df.groupby('courseOfferId')['fullAmount'].apply(sum)
by_timezone = pd.DataFrame({'courseOfferId':tmp.index, 'totalAmount':tmp}).sort_values(['totalAmount'], ascending = False).reset_index(drop=True)
st.dataframe(by_timezone.head(top_k_courses))

# Tenure
current_ts = datetime.today().strftime('%d-%m-%Y %H:%M')
n_students = df['id'].nunique()
top_k_tenure = st.sidebar.slider('Choose the Number of Students to Visualise Lifecycles', 0, n_students, (0, n_students), 1)[1]
st.subheader("Top Students by Lifecycle")
timedelta = df.apply(lambda row : pd.to_datetime(df['createTime'].max(), format='%d-%m-%Y %H:%M') - pd.to_datetime(row['createTime'], format='%d-%m-%Y %H:%M'), axis=1)
df['days'] = timedelta.dt.days
df['hours'] = timedelta.dt.components.hours
df['minutes'] = timedelta.dt.components.minutes
cols = ['id','firstName','lastName','days','hours','minutes']
st.dataframe(df[cols].head(top_k_tenure))

# st.subheader('Tenure Lifecycle')
# hist_values = np.histogram(df['days'].head(top_k_tenure), bins=100, range=(0,100))[0]
# st.bar_chart(hist_values)

#st.subheader('Tenure Lifecycle')
f = px.histogram(df.head(top_k_tenure), x="days", nbins=100, title="Lifecycle distribution")
f.update_xaxes(title="Lifecycle")
f.update_yaxes(title="No. of students")
st.plotly_chart(f)
