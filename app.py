# Import numpy and sqlalchemy dependencies
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
# importing flask and jsonify for serve set up
from flask import Flask, jsonify

# Database set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Setting up Flask
app = Flask(__name__)

# Creating the different flask routes
@app.route("/")
def welcome():
    """Return all of the available routes"""
    return(
        f"All of the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end>"

    )

# return a jsonified dictionary of precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():

    # variables needed
    most_recent_day = None
    past_year_precip_data = None

    # openning the session to pull queries in
    session = Session(engine)

    # finding the most recent date in data
    most_recent_day = session.query(Measurement.date).order_by((Measurement.date).\
        desc()).first()[0]
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.datetime.strptime(most_recent_day, "%Y-%m-%d") - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    past_year_precip_data = session.query(Measurement.date, Measurement.prcp).\
        order_by((Measurement.date).asc()).\
        filter(Measurement.date > one_year_ago).\
        filter(Measurement.prcp).all()

    # closing the session once data is pulled
    session.close()
    
    # convert the query results into a dictionary
    precipitation_data = []
    for date, prcp in past_year_precip_data:
        temp_diction = {}
        temp_diction['date'] = date
        temp_diction['prcp'] = prcp
        precipitation_data.append(temp_diction)

    #return the jsonified dictionary
    return(jsonify(precipitation_data))

# return a jsonified list of stations from the data set
@app.route("/api/v1.0/stations")
def station():

    # open a session
    session = Session(engine)

    # query for a list of stations within the dataset
    stations_list = session.query(Station.station, Station.name).all()

    # closing the session
    session.close()

    # returning the jsonified list of stations and station names
    return(jsonify(stations_list))

@app.route("/api/v1.0/tobs")
def tobs():
    #open session to query from
    session = Session(engine)

    # finding the most recent date in data
    most_recent_day = session.query(Measurement.date).order_by((Measurement.date).\
        desc()).first()[0]
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.datetime.strptime(most_recent_day, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the dates and tobs of the most active station for the last year
    most_active_station = session.query(Measurement.station).\
        order_by((Measurement.date).asc()).\
        filter(Measurement.date >= one_year_ago).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()[0][0]

    # getting precipitation data for most active station
    precip_data = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        order_by((Measurement.date).asc()).\
        filter(Measurement.date >= one_year_ago).all()

    # Closing the session
    session.close()

    # return a JSON list of temperature observations (tobs) for the previous year
    return(jsonify(precip_data))

@app.route("/api/v1.0/<start>")
def start(start=None):
    #Opening the session 
    session = Session(engine)

    # Query for the min, max, and avg temperatures for all dates greater than and equal to start date
    start_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    #closing the session
    session.close()

    #Returning the jsonified list of min, avg, max
    return(jsonify(start_date_query))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    #Opening the session 
    session = Session(engine)

    # Query for the min, max, and avg temperatures for all dates greater than and equal to start date
    # and less than and equal to the end date
    start_end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    #closing the session
    session.close()

    #Returning the jsonified list of min, avg, max
    return(jsonify(start_end_query))


# End sequence for Flask
if __name__ == '__main__':
    app.run(debug=True)