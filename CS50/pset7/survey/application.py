import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


# Validate form submission and write the form's values to a csv file called survey.csv
@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("name") or not request.form.get("school") or not request.form.get("subject"):
        return render_template("error.html")
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("school"), request.form.get("subject")))
    file.close()
    return redirect("/sheet")


# Read survey.csv and display the submissions to a table
@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    students = list(reader)
    return render_template("sheet.html", students=students)


