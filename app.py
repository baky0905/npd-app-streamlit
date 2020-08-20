# simple_streamlit_app.py
"""
# NPD Wells
"""

import plotly.express as px
import numpy as np
import pandas as pd
import streamlit as st

st.title("NPD Wells")

st.write("Lets take a peak at the dataframe")

data = pd.read_csv("./data/wellbore_exploration_all.csv")
data['spud_year'] = pd.DatetimeIndex(data['wlbCompletionDate']).year


min_year = int(data['spud_year'].min())
max_year = int(data['spud_year'].max())

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Completion date range:',
    min_year, max_year, ((max_year-10), max_year)
)

# Select
add_selectbox = st.sidebar.selectbox(
    'Choose main area:',
    data["wlbMainArea"].unique()
)

mask = (data['spud_year'] >= add_slider[0]) & (
    data['spud_year'] <= add_slider[1]) & (data['wlbMainArea'] == add_selectbox)

data = data[mask]

data


st.write(f"Wells filtered are between {add_slider[0]} and {add_slider[1]}")
st.write(f"Number of wells after filtering: {data['wlbWellboreName'].count()}")


map = px.scatter_mapbox(
    data, lat="wlbNsDecDeg",
    lon="wlbEwDesDeg",
    color="wlbPurpose",
    size="wlbWaterDepth",
    # color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15,
    zoom=10,
    mapbox_style="carto-positron")
map

heat = px.density_contour(
    data,
    x="wlbDrillingDays",
    y="wlbTotalDepth",
    color="wlbMainArea",
    marginal_x="histogram",
    marginal_y="histogram")
heat

d3 = fig = px.scatter_3d(
    data,
    x="wlbNsDecDeg",
    y="wlbEwDesDeg",
    z="wlbTotalDepth",
    color="wlbContent",
    size="spud_year",
    hover_name="wlbWellboreName",
    # symbol="wlbContent",
    # color_discrete_map={"Joly": "blue", "Bergeron": "green", "Coderre": "red"}
)

d3


# option = st.sidebar.selectbox(
#     'Which number do you like best?',
#     data['wlbWellboreName'])

# 'You selected:', option
