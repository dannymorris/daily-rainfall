from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from meteostat import Hourly, units

def get_hourly_weather(station, start_date, end = datetime.now()):
    df = Hourly(station, start = start_date, end = end).convert(units.imperial).fetch().reset_index()
    df['time_date'] = df['time'].dt.date
    return(df)