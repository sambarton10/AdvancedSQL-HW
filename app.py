import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/Precipitation<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/TOBs<br/>"
        f"/api/v1.0/Start_Only<br/>"
    )

@app.route("/api/v1.0/Precipitation")
def Precipitation():
    # Create our session (link) from Python to the DB
    
    precip = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    all_precip_data = list(np.ravel(precip))
    return jsonify(all_precip_data)

@app.route("/api/v1.0/Stations")
def Stations():
    # Create our session (link) from Python to the DB
    
    station = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    session.close()
    
    all_station_data = []
    for station, name, latitude, longitude, elevation in station:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_station_data.append(station_dict)

    return jsonify(all_station_data)
           
@app.route("/api/v1.0/TOBS")
def TOBS():
    # Create our session (link) from Python to the DB
    
    tob = session.query(Measurement.station, Measurement.date, Measurement.tobs).group_by(Measurement.date).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station=="USC00519281").all()
    
    session.close()
    
    tob_list = []
    for station, date, tobs in tob:
        tob_dict = {}
        tob_dict["station"] = station
        tob_dict["date"] = date
        tob_dict["tobs"] = tobs
        tob_list.append(tob_dict)
        
    return jsonify(tob_list)

@app.route("/api/v1.0/<start>")
def start_only(start):
    # Create our session (link) from Python to the DB
    
    canonicalized = start.replace(" ", "")
    start_query = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    data1 = list(np.ravel(start_query))
    return jsonify(data1)


@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    # Create our session (link) from Python to the DB
    
    start = start.replace(" ", "")
    new_end = end.replace(" ", "")
    
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    session.close()

    data2 = list(np.ravel(results))
    return jsonify(data2)
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    