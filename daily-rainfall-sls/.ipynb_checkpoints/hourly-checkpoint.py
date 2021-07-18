import json
from datetime import datetime, timedelta
import pandas as pd
from meteostat import Stations, Daily, Hourly, units

def get_hourly_weather(event, context):
    station = event['station']
    days_history = event['days_history']
    end = datetime.now()
    df = Hourly(station,
                start = datetime.now() - timedelta(days = days_history), 
                end = end).convert(units.imperial).fetch().reset_index()
    df['time_date'] = df['time'].dt.date
    response = {
        "statusCode": 200,
        "body": json.dumps(df.to_json(orient = "split"))
    }
    return(response)