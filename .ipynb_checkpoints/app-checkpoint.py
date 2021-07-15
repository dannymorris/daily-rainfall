from datetime import datetime, timedelta
import streamlit as st
import numpy as np
import pandas as pd
from meteostat import Stations, Daily, Hourly, units

def get_station(lat, long, n=1):
    """Get the weather station(s) nearest to a lat-long coordinate"""
    stations = Stations().nearby(lat, long)
    station = stations.fetch(n)
    return(station)

def get_daily_weather(station, start_date, end = datetime.now()):
    df = Daily(station, start=start_date, end=end).convert(units.imperial).fetch().reset_index()
    return(df)

run_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

stations = (Stations().fetch()
    .query('country == "US"')
    .pipe(lambda x: x.assign(station_long_name = x['name'] + ", " + x['region']))        
    .reset_index()
)

########
## UI ##
########

state_selectbox = st.sidebar.selectbox(
    "Select a state",
    stations['region'].unique()
)

station_selectbox = st.sidebar.selectbox(
    "Select a weather station",
    stations['name'].loc[stations["region"] == state_selectbox]
)

selected_station = stations["id"].loc[(stations["name"] == station_selectbox) & (stations["region"] == state_selectbox)].to_list()

daily_weather = get_daily_weather(station = selected_station, 
                                  start_date = datetime.now() - timedelta(days=60+28))

daily_stats = (daily_weather
    .pipe(lambda x: x.assign(time = x['time'].dt.date))
    .pipe(lambda x: x.assign(prcp = x['prcp'].fillna(0)))
    .pipe(lambda x: x.assign(total_prcp_7_days = x['prcp'].rolling(7).sum()))
    .pipe(lambda x: x.assign(total_prcp_14_days = x['prcp'].rolling(14).sum()))
    .pipe(lambda x: x.assign(total_prcp_28_days = x['prcp'].rolling(28).sum()))
    .pipe(lambda x: x.assign(avg_tmax_7_days = x['tmax'].rolling(7).mean()))
    .pipe(lambda x: x.assign(avg_tmin_7_days = x['tmin'].rolling(7).mean()))
    .loc[:, ['time', 'prcp', 'total_prcp_7_days', 'total_prcp_14_days', 'total_prcp_28_days', 'avg_tmax_7_days', 'avg_tmin_7_days']]
    .dropna()
    .rename(columns = {"time": "index"})
    .set_index(['index'])
    .sort_index(ascending=False)
)

st.title('Rainfall Trends')

st.write("Last updated: " + run_dt)

st.line_chart(daily_stats[['prcp', 'total_prcp_7_days', 'total_prcp_28_days']])

st.dataframe(daily_stats[['prcp', 'total_prcp_7_days', 'total_prcp_28_days']].head(10))