import os
import cs50
import math

from cs50 import SQL
from flask import Flask, redirect, render_template, request

# https://docs.python.org/2/library/operator.html
from operator import itemgetter

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Make sure responses aren't cached
@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///feeling-color.db")


@app.route("/", methods=["GET"])
def get_index():
    db.execute("UPDATE relations SET distance = ''")
    # return redirect("/form")
    return redirect("/begin")


# Homepage, for GET method
@app.route("/begin", methods=["GET"])
def get_home():
    return render_template("home.html")


# When the form on home.html is submitted, redirect to /form
@app.route("/begin", methods=["GET","POST"])
def post_home():
    return redirect("/form")


# Show form
@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")

# Dased on the inputed color from the submitted form, perform calculations
@app.route("/form", methods=["POST"])
def post_form():
    # Validate form submission
    if not request.form.get("colorselection"):
        return render_template("error.html")

    # Convert the rgb string with id colorpicker to a list of only the rgb values as integers
    colorInput = request.form.get("colorselection")[4:-1]
    inputRgb = colorInput.split(",")
    intRgb = list(map(int, inputRgb))

    # For each rgb string in the color field from the relations table, convert it to a list ('r','g','b'), then convert to int and append to the initialized colors_set_list
    colors_set = db.execute("SELECT colorRgb FROM relations")
    colors_set_list = []
    for pair in range(len(colors_set)):
        colors_set_list.append(list(map(int, colors_set[pair]['colorRgb'].split(","))))

    # Calculate Euclidean distance (using the RGB triples of the colors) between the input color and each color in the database
    dists_list = []
    for color in colors_set_list:
        d_r = abs(intRgb[0] - color[0])
        d_g = abs(intRgb[1] - color[1])
        d_b = abs(intRgb[2] - color[2])
        dist = math.sqrt(d_r ** 2 + d_g ** 2 + d_b ** 2)
        dists_list.append(dist)

    # Upload the distances to the database corresponding to the right color
    for d in range(len(dists_list)):
        db.execute("UPDATE relations SET distance = :dist WHERE id = :color_id", dist = dists_list[d], color_id=d+1)

    # Extract colorname-colorRGBstring-associatedemotion-distance combos from the database
    combo = db.execute("SELECT colorName, colorRgb, emotAssoc, distance FROM relations")
    # Sort each combo by distance (shortest to longest distance) via itemgetter from https://docs.python.org/2/library/operator.html
    sortedCombos = sorted(combo, key=itemgetter('distance'))
    # Take the top 3 of the sorted list to get the top 3 associations with the input color
    top3 = sortedCombos[:3]
    # Initialize separate lists for the values of each key
    top3cols = []
    top3emos = []
    top3dists = []
    top3rgb = []
    # Create lists
    for elem in top3:
        top3cols.append(elem['colorName'])
        top3rgb.append(elem['colorRgb'])
        top3emos.append(elem['emotAssoc'])
        top3dists.append(elem['distance'])

    # Initialize lists for proportions and scaled percents
    propsRaw = []
    percsScaled = []
    # For each of the top 3 distances, calculate 1/(d+1) to get a proportion; this formula makes sense because the smaller the distance the larger the fraction and so the larger the association; there is +1 so that there is never a zero denominator
    for d in top3dists:
        propsRaw.append(1 / (d+1))
    sumProps = sum(propsRaw)
    # For each proportion, scale it by 1/(sum of the three proportions) so that the sum of the three resulting numbers adds up to 1; then convert to percent with no decimal places
    for p in propsRaw:
        percsScaled.append("%.0f%%" % (100 * p / sumProps))

    return render_template("results.html", color=request.form.get("colorselection"), cols=top3cols, emos=top3emos, percs=percsScaled, rgbs=top3rgb)

# Takes you to About page
@app.route("/about", methods=["GET"])
def about():
        return render_template("about.html")


# Takes you to Survey page
@app.route("/survey", methods=["GET"])
def survey():
        return render_template("survey.html")


# Takes you to Contact page
@app.route("/contact", methods=["GET"])
def contact():
        return render_template("contact.html")




