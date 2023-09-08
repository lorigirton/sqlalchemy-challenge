# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
station=Base.classes.station
measurement=Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        "Welcome to the Surfs Up API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/{start}<br/>"
        "/api/v1.0/{start}/{end}<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= dt.date(2016, 8, 23)).all()
    clean_results = {}

    for row in results:
        date= row[0]
        prcp= row[1]
        clean_results[date]=prcp

    session.close()
    return jsonify(clean_results)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(measurement.station).all()
    station_results = []

    for row in results:
        station= row[0]
        station_results.append(station) 

    session.close()  
    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
    results= session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= dt.date(2016, 8, 23)).all()

    tobs_results = {}

    for row in results:
        date= row[0]
        tobs= row[1]
        tobs_results[date]=tobs

    session.close()
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start(start):
    results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

