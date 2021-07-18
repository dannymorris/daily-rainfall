from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from meteostat import Hourly, units

def get_hourly_weather(station, days_history = 30, end = datetime.now()):
    df = Hourly(station, start = datetime.now() - timedelta(days=days_history), end = end).convert(units.imperial).fetch().reset_index()
    df['time_date'] = df['time'].dt.date
    return(df)
