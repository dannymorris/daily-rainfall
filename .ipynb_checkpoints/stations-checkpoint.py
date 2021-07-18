from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from meteostat import Stations

def get_stations():
    stations = (Stations().fetch()
        .query('country == "US"')
        .reset_index()
    )
    return(stations)