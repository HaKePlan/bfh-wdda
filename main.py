import sqlite3

from flask import Flask, render_template, request

from scripts.exercise_b import get_announcement_by_year_build, get_announcement_by_city_name

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('./project_data.sqlite')
    return conn


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/year")
def build_after_year():
    try:
        year = int(request.args.get("year"))
    except ValueError:
        return {"message": "please provide a valid year as a number"}, 400

    number_of_announcements = get_announcement_by_year_build(get_db_connection(), year)[0][0]

    print(number_of_announcements)

    return render_template("by_year.html", year=year, count=number_of_announcements)


@app.route("/city")
def filter_by_city_name():
    try:
        city = request.args.get("city")
    except ValueError:
        return {"message": "please provide a valid city name as string"}, 400

    announcement_by_city = get_announcement_by_city_name(get_db_connection(), city)

    return render_template("by_city.html", name=city, rows=announcement_by_city)




