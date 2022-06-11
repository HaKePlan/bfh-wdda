import sqlite3

from flask import Flask, render_template, request

from scripts.exercise_b import get_announcement_by_year_build, get_announcement_by_city_name

# Initiate flask application
app = Flask(__name__)


def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect('./project_data.sqlite')
    return conn


@app.route("/")
def home():
    """Route to indexpage"""
    return render_template('home.html')


@app.route("/year")
def build_after_year():
    """Return all houses which ar build after a given year"""
    try:
        # validate input from url params
        year = int(request.args.get("year"))
    except ValueError:
        return {"message": "please provide a valid year as a number"}, 400

    # create connection to db and fetch all houses build after year
    conn = get_db_connection()
    number_of_announcements = get_announcement_by_year_build(conn, year)[0][0]
    conn.close()

    # return rendered html
    return render_template("by_year.html", year=year, count=number_of_announcements)


@app.route("/city")
def filter_by_city_name():
    """Return all announcements in a given city"""
    try:
        # try to get the city name from url param
        city = request.args.get("city")
    except ValueError:
        return {"message": "please provide a valid city name as string"}, 400

    # create connection to db and fetch all announcements in a city
    conn = get_db_connection()
    announcement_by_city = get_announcement_by_city_name(conn, city)
    conn.close()

    # return rendered html
    return render_template("by_city.html", name=city, rows=announcement_by_city)




