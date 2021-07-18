from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from meteostat import Daily, units

def get_daily_weather(station, start_date, end = datetime.now()):
    df = Daily(station, start=start_date, end=end).convert(units.imperial).fetch().reset_index()
    return(df)