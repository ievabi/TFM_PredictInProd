from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from datetime import datetime
import pytz
import joblib
from predict import get_model

from predict import PATH_TO_LOCAL_MODEL, download_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(pickup_datetime,
          pickup_longitude,
          pickup_latitude,
          dropoff_longitude,
          dropoff_latitude,
          passenger_count):


# create a datetime object from the user provided datetime
    pickup_datetime = "2021-05-30 10:12:00"
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

# localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
# localize the datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
# convert a datetime to the format expected by the pipeline
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
# Final dictionary
    dict = {"key":["2013-07-06 17:18:00.000000119"],
            "pickup_datetime": [formatted_pickup_datetime],
            "pickup_longitude": [float(pickup_longitude)],
            "pickup_latitude": [float(pickup_latitude)],
            "dropoff_longitude": [float(dropoff_longitude)],
            "dropoff_latitude": [float(dropoff_latitude)],
            "passenger_count": [int(passenger_count)]}
    X_pred = pd.DataFrame(dict)

    pipeline = get_model(PATH_TO_LOCAL_MODEL)
    y_pred = round(float(pipeline.predict(X_pred)[0]),3)
    prediction = {'fare': y_pred}

    return prediction
