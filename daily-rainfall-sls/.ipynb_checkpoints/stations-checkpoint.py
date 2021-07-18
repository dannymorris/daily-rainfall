import json
from datetime import datetime, timedelta
import pandas as pd
from meteostat import Stations, Daily, Hourly, units

def get_stations(event, context):
    stations = (Stations().fetch()
        .query('country == "US"')
        .reset_index()
    )
    stations['country'] = stations['country'].astype(str)
    stations['region'] = stations['region'].astype(str)
    response = {
        "statusCode": 200,
        "body": json.dumps(stations.to_json(orient = "split"))
    }
    return(response)

