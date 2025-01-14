# Import the dependencies.
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
@app.route("/")
def welcome():
        return(
            f"You're on the Hawaii Climate Analysis API Homepage <br/>"
            f"Available Routes: <br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/temp/start<br/>"
            f"/api/v1.0/temp/start/end<br/>"
            f"<p> 'start' and 'end' date should be in the format MMDDYYYY.</p>"
            )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Display the precipitation data for the last year"""
    last_year=dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>= last_year).all()
    session.close()
    precip_dictionary = {date:prcp for date, prcp in precipitation}

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
   # precipitation_df = pd.DataFrame(precipitation, columns=['Date', 'Precipitation'])
    return jsonify(precip_dictionary)

   
 


#################################################
# Flask Routes
#################################################
