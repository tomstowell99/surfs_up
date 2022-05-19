# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:26:01 2022

@author: M062896
"""

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# allows us to access and query our sqlite database file
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

# reflect to the database
Base.prepare(engine, reflect=True)

# save our references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station
# create our session link
session = Session(engine)

# set up our flask
app = Flask(__name__)

@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# new route
@app.route("/api/v1.0/precipitation")

# date one year ago from most recent date in db and pull back precip
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
      # this part converts to json so we can so we can look at attribue pairs. date and precip
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
   

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    # the stations = stations formats our lists into json
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    # calc date from one year ago from most current date in dg
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    # jsonify or temps like we did for stations
    return jsonify(temps=temps)



@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)




