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
        desc()).first()
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    past_year_precip_data = session.query(Measurement.date, Measurement.prcp).\
        order_by((Measurement.date).asc()).\
        filter(Measurement.date > one_year_ago).\
        filter(Measurement.prcp).all()

    # closing the session once data is pulled
    session.close()


@app.route("/api/v1.0/stations")
def station():
    return("hello")

@app.route("/api/v1.0/tobs")
def tobs():
    return("hello")

@app.route("/api/v1.0/<start>")
def start():
    return("hello")

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    return("hello")


# End sequence for Flask
if __name__ == '__main__':
    app.run(debug=True)