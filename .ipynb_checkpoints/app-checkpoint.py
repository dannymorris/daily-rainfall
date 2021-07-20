from datetime import datetime, timedelta
import streamlit as st
import numpy as np
import pandas as pd
from meteostat import Stations, Daily, Hourly, units

from hourly import *
from daily import *
from stations import *


run_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

stations = get_stations()

########
## UI ##
########

states = stations['region'].unique()

state_selectbox = st.sidebar.selectbox(
    "Select a state",
    states,
    index = list(states).index("NY")
)

station_names = stations['name'].loc[stations['region'] == state_selectbox]

names_selectbox = st.sidebar.selectbox(
    "Select a weather station",
    station_names,
    index = list(station_names).index('Niagara Falls / Walmore')
)

def get_station_id(stations_df, state, name):
    out = stations_df["id"].loc[(stations_df['name'] == name) & (stations_df['region'] == state)].to_list()
    return(out)

selected_station = get_station_id(stations, state_selectbox, names_selectbox)

hourly_weather = get_hourly_weather(station = selected_station, 
                                    days_history = 90)

daily_prec = (hourly_weather
    .groupby('time_date')
    .agg({'prcp': 'sum'})
    .pipe(lambda x: x.assign(total_prcp_7_days = x['prcp'].rolling(7).sum()))
    .pipe(lambda x: x.assign(total_prcp_30_days = x['prcp'].rolling(30).sum()))
    .reset_index()
    .sort_values(['time_date'], ascending = False)
    .head(60)
    .rename(columns = {'prcp': "Total_Daily",
                      'total_prcp_7_days': "7_Day_Total",
                      'total_prcp_30_days': '30_Day_Total'})
    .pipe(lambda x: pd.melt(x, id_vars = ['time_date'], 
                            value_vars = ['Total_Daily', '7_Day_Total', '30_Day_Total']))
)

st.title('Rainfall Trends')

st.write("Last updated: " + run_dt)

st.write("Daily and Running Totals (Last 60 Days)")

st.vega_lite_chart(
    data = daily_prec,
    spec = {
        "mark": {
            "type": "line", 
            "strokeWidth": 2,
            "point": True,
            "tooltip": True
        },
        "width": 600,
        "height": 350,
        'encoding': {
            'x': {'field': 'time_date', 
                  'type': 'temporal', 
                  "axis": {"format": "%b-%d", "title": "Date", "grid": False},
                  'tooltip': True},
            'y': {'field': 'value', 
                  'type': 'quantitative',
                  "scale": {"padding": 10, 'domainMin': 0, 'domainMax': 13}},
            "color": {"field": "variable", 
                      "type": "ordinal"}
        }
    }
)

st.write("Hourly Totals (Last 24 Hours)")

st.vega_lite_chart(
    data = hourly_weather.tail(24),
    spec = {
        "mark": {
            "type": "line", 
            "strokeWidth": 2,
            "point": True,
            "tooltip": True
        },
        "width": 600,
        "height": 350,
        'encoding': {
            'x': {'field': 'time', 
                  'type': 'temporal', 
                  "axis": {"title": "Date", "grid": False},
                  'tooltip': True},
            'y': {
                'field': 'prcp',
                'type': 'quantitative',
                'scale': {
                    'padding': 10,
                    'domainMin': 0,
                    'domainMax': 1
                    }
                 },
        }
    }
)