from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, desc
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from config import connection_string, secret_key, dan_id
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

#%% set up

# application set up
app = Flask(__name__)
app.secret_key = secret_key
app.permanent_session_lifetime = timedelta(minutes = 5)


#%% database set up
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
Base = declarative_base()

class Intake(Base):   
    __tablename__ = 'intake'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable = False)
    intake_ml = Column(Integer, nullable = False)
    measurement_time = Column(DateTime, nullable = False)
    created_time = Column(DateTime, nullable = False)
    active = Column(Boolean, nullable = False)

    def __init__(self, user_id, intake_ml, measurement_time):
        self.user_id = user_id 
        self.intake_ml = intake_ml 
        self.measurement_time = datetime.strptime(measurement_time, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
        self.created_time = datetime.now()
        self.active = True

class Output(Base):   
    __tablename__ = 'output'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable = False)
    output_ml = Column(Integer, nullable = False)
    measurement_time = Column(DateTime, nullable = False)
    created_time = Column(DateTime, nullable = False)
    active = Column(Boolean, nullable = False)

    def __init__(self, user_id, output_ml, measurement_time):
        self.user_id = user_id 
        self.output_ml = output_ml 
        self.measurement_time = datetime.strptime(measurement_time, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
        self.created_time = datetime.now()
        self.active = True

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#%% set up pages

@app.route("/")
def home():
    return redirect(url_for("log"))

@app.route("/intake", methods = ["POST", "GET"])
def intake():
    if request.method == "POST":
        intake_ml = request.form["intake"]
        intake_timestamp = request.form["timestamp"]
        new_intake = Intake(user_id = dan_id, intake_ml = intake_ml, measurement_time = intake_timestamp)
        session.add(new_intake)
        session.commit()
        flash("Intake Logged", "intake_success")
        return redirect(url_for("log"))
    else:       
        return render_template("intake.html")

@app.route("/output", methods = ["POST", "GET"])
def output():
    if request.method == "POST":
        output_ml = request.form["output"]
        output_timestamp = request.form["timestamp"]
        new_output = Output(user_id = dan_id, output_ml = output_ml, measurement_time = output_timestamp)
        session.add(new_output)
        session.commit()   
        flash("Output Logged", "output_success")
        return redirect(url_for("log"))
    else:       
        return render_template("output.html")

@app.route("/log")
def log():
    # Retrieve the most recent 10 records from the database tables
    intake_data = session.query(Intake).filter(Intake.active == True).order_by(Intake.created_time.desc()).limit(10)
    output_data = session.query(Output).filter(Output.active == True).order_by(Output.created_time.desc()).limit(10)

    return render_template("log.html", intake_data=intake_data, output_data=output_data)    

@app.route("/delete_intake/<int:intake_id>", methods = ["POST"])
def delete_intake(intake_id):
    intake = session.query(Intake).filter_by(id=intake_id).first()
    # Check if the intake record exists
    if intake:
        # Update the active field to False
        intake.active = False
        session.commit()
        flash("Intake deleted successfully", "delete_success")
    else:
        flash("Intake record not found", "delete_error")

    return redirect(url_for("log"))

@app.route("/delete_output/<int:output_id>", methods = ["POST"])
def delete_output(output_id):
    output = session.query(Output).filter_by(id=output_id).first()
    # Check if the intake record exists
    if output:
        # Update the active field to False
        output.active = False
        session.commit()
        flash("Output deleted successfully", "delete_success")
    else:
        flash("Output record not found", "delete_error")

    return redirect(url_for("log"))

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


if __name__ == "__main__":
    app.run(debug = True)