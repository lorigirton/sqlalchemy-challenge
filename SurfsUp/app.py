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
    return jsonify(session.query(measurement.date, measurement.prcp).all())

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(session.query(station.station).all())

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(session.query(measurement.date, measurement.tobs).filter(measurement.station=='USC00519281').all())

@app.route("/api/v1.0/<start>")
def start(start):
    return jsonify(session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all())

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    return jsonify(session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all())

if __name__ == "__main__":
    app.run(debug=True)

session.close()

