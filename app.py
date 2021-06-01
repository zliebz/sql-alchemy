#### Imports & Setup
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

#### Database work
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

## -----------------------------------------------------------------------

#### Session link
session = Session(engine)

## -----------------------------------------------------------------------

#### Flask
app = Flask(__name__)

@app.route("/")

## -----------------------------------------------------------------------

#### Returns

def Home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

## -----------------------------------------------------------------------

#### Precipiation Route
@app.route("/api/v1.0/precipitation")
def percipitation():

    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    first_date = last_date - timedelta(days = 365)
    prcp_results = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).order_by(Measurement.date).all())
    return jsonify(prcp_results)

## -----------------------------------------------------------------------

#### Stations

@app.route("/api/v1.0/stations")
def stations():
  session  = Session(engine)
  stations_results = session.query(Station.station, Station.name).all()
  return jsonify(stations_results)

## -----------------------------------------------------------------------

#### Tobs

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    first_date = last_date - timedelta(days = 365)
    station_counts = (session.query(Measurement.station, func.count).filter(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    top_sation = (station_counts[0])
    top_station = (top_station[0])
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == top_station).all()
    top_station_year_obs = session.query(Measurement.tobs).\
    filter(Measurement.station == top_station).filter(Measurement.date >= first_date).all()
    return jsonify(top_station_year_obs)

## -----------------------------------------------------------------------

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start(start = none, end = none):
    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)        

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
  
    return jsonify(results)


if __name__ == '__main__':
    app.run()
