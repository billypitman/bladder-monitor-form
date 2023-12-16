import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import timedelta
import pytz

# TODO: generalize timezones to the web form user
timezone = pytz.timezone(os.environ["TZ"])
# TODO: generalize with uesr login
user_id = 1

# app and database set up
connection_string = (
    f"mssql+pyodbc:///?odbc_connect={os.environ['DATABASE_CONNECTION_STRING']}"
)
secret_key = os.environ["SECRET_KEY"]
app = Flask(__name__)
app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)


class Intake(db.Model):
    __tablename__ = "intake"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    intake_ml = db.Column(db.Integer, nullable=False)
    measurement_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.VARCHAR(50), nullable=False)

    def __init__(self, user_id, intake_ml, measurement_time, type):
        self.user_id = user_id
        self.intake_ml = intake_ml
        self.measurement_time = datetime.strptime(
            measurement_time, "%Y-%m-%dT%H:%M"
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.created_time = datetime.now()
        self.active = True
        self.type = type


class Output(db.Model):
    __tablename__ = "output"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    output_ml = db.Column(db.Integer, nullable=False)
    measurement_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    urgency = db.Column(db.VARCHAR(50), nullable=False)

    def __init__(self, user_id, output_ml, measurement_time, urgency):
        self.user_id = user_id
        self.output_ml = output_ml
        self.measurement_time = datetime.strptime(
            measurement_time, "%Y-%m-%dT%H:%M"
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.created_time = datetime.now()
        self.active = True
        self.urgency = urgency


# ### set up pages


@app.route("/")
def home():
    return redirect(url_for("log"))


@app.route("/intake", methods=["POST", "GET"])
def intake():
    if request.method == "POST":
        intake_ml = request.form["intake"]
        intake_timestamp = request.form["timestamp"]
        intake_type = request.form["type"]
        new_intake = Intake(
            user_id=user_id,
            intake_ml=intake_ml,
            measurement_time=intake_timestamp,
            type=intake_type,
        )
        db.session.add(new_intake)
        db.session.commit()
        flash("Intake Logged", "intake_success")
        return redirect(url_for("log"))
    else:
        return render_template(
            "intake.html", current_datetime=datetime.now().strftime("%Y-%m-%d %H:%M")
        )


@app.route("/output", methods=["POST", "GET"])
def output():
    if request.method == "POST":
        output_ml = request.form["output"]
        output_timestamp = request.form["timestamp"]
        output_urgency = request.form["urgency"]
        new_output = Output(
            user_id=user_id,
            output_ml=output_ml,
            measurement_time=output_timestamp,
            urgency=output_urgency,
        )
        db.session.add(new_output)
        db.session.commit()
        flash("Output Logged", "output_success")
        return redirect(url_for("log"))
    else:
        return render_template(
            "output.html", current_datetime=datetime.now().strftime("%Y-%m-%d %H:%M")
        )


@app.route("/log")
def log():
    # Retrieve the most recent 10 records from the database tables
    intake_data = (
        db.session.query(Intake)
        .filter(Intake.active == True)
        .order_by(Intake.created_time.desc())
        .limit(10)
    )
    output_data = (
        db.session.query(Output)
        .filter(Output.active == True)
        .order_by(Output.created_time.desc())
        .limit(10)
    )

    return render_template("log.html", intake_data=intake_data, output_data=output_data)


@app.route("/delete_intake/<int:intake_id>", methods=["POST"])
def delete_intake(intake_id):
    intake = db.session.query(Intake).filter_by(id=intake_id).first()
    # Check if the intake record exists
    if intake:
        # Update the active field to False
        intake.active = False
        db.session.commit()
        flash("Intake deleted successfully", "delete_success")
    else:
        flash("Intake record not found", "delete_error")

    return redirect(url_for("log"))


@app.route("/delete_output/<int:output_id>", methods=["POST"])
def delete_output(output_id):
    output = db.session.query(Output).filter_by(id=output_id).first()
    # Check if the intake record exists
    if output:
        # Update the active field to False
        output.active = False
        db.session.commit()
        flash("Output deleted successfully", "delete_success")
    else:
        flash("Output record not found", "delete_error")

    return redirect(url_for("log"))


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
