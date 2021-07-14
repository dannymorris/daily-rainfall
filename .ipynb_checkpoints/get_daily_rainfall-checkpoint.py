from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from meteostat import Stations, Daily, Hourly, units

def get_station(lat, long, n=1):
  """Get the weather station(s) nearest to a lat-long coordinate"""
  stations = Stations().nearby(lat, long)
  station = stations.fetch(n)
  return(station)

def get_daily_weather(station, start_date, end = datetime.now()):
  df = Daily(station, start=start_date, end=end).convert(units.imperial).fetch().reset_index()
  return(df)

def get_hourly_weather(station, start_date, end = datetime.now()):
  df = Hourly(station, start=start_date, end=end).convert(units.imperial).fetch().reset_index()
  return(df)

station = get_station(lat=43.0505, long=-78.8766, n=1)

daily_weather = get_daily_weather(station=station, start_date = datetime.now() - timedelta(days=60+28))

daily_stats = (daily_weather
    .pipe(lambda x: x.assign(prcp = x['prcp'].fillna(0)))
    .pipe(lambda x: x.assign(total_prcp_7_days = x['prcp'].rolling(7).sum()))
    .pipe(lambda x: x.assign(total_prcp_14_days = x['prcp'].rolling(14).sum()))
    .pipe(lambda x: x.assign(total_prcp_28_days = x['prcp'].rolling(28).sum()))
    .pipe(lambda x: x.assign(avg_tmax_7_days = x['tmax'].rolling(7).mean()))
    .pipe(lambda x: x.assign(avg_tmin_7_days = x['tmin'].rolling(7).mean()))
    .loc[:, ['time', 'prcp', 'total_prcp_7_days', 'total_prcp_14_days', 'total_prcp_28_days', 'avg_tmax_7_days', 'avg_tmin_7_days']]
    .dropna()
)

hourly_weather = get_hourly_weather(station = station,
                                    start_date = datetime.now() - timedelta(days = 60*28))
                                    
hourly_stats = (hourly_weather
    .pipe(lambda x: x.assign(date = x['time'].dt.date))
    .pipe(lambda x: x.assign(prcp = x['prcp'].fillna(0)))
    .groupby(['date'])
    .agg({'prcp': 'sum', 'temp': ['max', 'min']})
    .reset_index()
    .pipe(lambda x: x.assign(total_prcp_7_days = x['prcp'].rolling(7).sum()))
    .pipe(lambda x: x.assign(total_prcp_14_days = x['prcp'].rolling(14).sum()))
    .pipe(lambda x: x.assign(total_prcp_28_days = x['prcp'].rolling(28).sum()))
    # .pipe(lambda x: x.assign(avg_tmax_7_days = x['tmax'].rolling(7).mean()))
    # .pipe(lambda x: x.assign(avg_tmin_7_days = x['tmin'].rolling(7).mean()))
    # .loc[:, ['time', 'prcp', 'total_prcp_7_days', 'total_prcp_14_days', 'total_prcp_28_days', 'avg_tmax_7_days', 'avg_tmin_7_days']]
    # .dropna()
)
        
hourly_stats                               
