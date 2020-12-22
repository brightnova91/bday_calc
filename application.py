import os
import datetime

from cs50 import SQL
from flask import Flask, render_template, request, redirect

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

today = datetime.datetime.now()
year = today.year
date = today.strftime("%b %d")

@app.route("/")
def index():
    """Show home page, show who has a bday today!"""
    # Query database for transactions
    query = "SELECT * FROM \"birthdays\" WHERE \"b_date\" = :sql_date"
    rows = db.execute(query, sql_date=date)

    return render_template("index.html", year=year, date=date, rows=rows)

@app.route("/list", methods=["GET", "POST"])
def list():
    """Show all people with the same bday!"""
    if request.method == "GET":
        return render_template("list.html")
    else:
        month = request.form.get("month")
        day = request.form.get("day")
        if int(day) < 10:
            day = "0"+day
        b_date = month + " " + day

        if not b_date:
            b_date = date
        else:
            query = "SELECT * FROM \"birthdays\" WHERE \"b_date\" = :sql_date"
            rows = db.execute(query, sql_date=b_date)
            return render_template("list.html", date=b_date, rows=rows)

@app.route("/compare", methods=["GET", "POST"])
def compare():
    """Show the bdays of 2 people, see who is older and by how much!"""
    query = "SELECT name FROM \"birthdays\" ORDER BY name ASC"
    rows = db.execute(query) #Collect all names for autocomplete feature

    ac_arr = "" #autocomplete array
    for row in rows:
        ac_arr += row["name"]+", "

    if request.method == "GET":
        return render_template("compare.html", ac_arr=ac_arr)
    else:
        name1 = request.form.get("name1")
        name2 = request.form.get("name2")
        bday1 = db.execute("SELECT b_date, b_year FROM \"birthdays\" WHERE name = :name", name = name1)
        bday2 = db.execute("SELECT b_date, b_year FROM \"birthdays\" WHERE name = :name", name = name2)

        date1 = ""
        date2 = ""

        for row in bday1:
            date1 += row["b_date"]+", "
            date1 += row["b_year"]

        for row in bday2:
            date2 += row["b_date"]+", "
            date2 += row["b_year"]

        return render_template("compare.html", ac_arr=ac_arr, name1=name1, bday1=date1, name2=name2, bday2=date2)
@app.route("/sort", methods=["GET", "POST"])
def sort():
    """Show list of birthdays"""
    if request.method == "GET":
        rows = db.execute("SELECT * FROM \"birthdays\"")

        #return apology("TODO")
        return render_template("sort.html",rows=rows)
    else:
        sortfield = request.form.get("sortfield")
        if sortfield == "b_year":
            sortfield = "cast("+sortfield+" as int)"

        query = "SELECT * FROM \"birthdays\" ORDER BY "+sortfield+" ASC"
        rows = db.execute(query)
        return render_template("sort.html",rows=rows)

@app.route("/signs", methods=["GET", "POST"])
def signs():
    """Show list of birthdays"""
    if request.method == "GET":

        #return apology("TODO")
        return render_template("signs.html")
    else:
        z_type = request.form.get("z_type") #did user pick Astrological/Chinese Zodiac?
        z_sign = request.form.get("z_sign") #Which Astrological sign was picked?
        c_sign = request.form.get("c_sign") #Which Chinese sign was picked?
        z_name = request.form.get("z_name") #What label does the sign have?

        if z_type == "z_sign":
            sign = z_sign #example: Virgo: "8,23-9,22"
            x = sign.split("-")
            sign_start = x[0] #8,23
            sign_end = x[1] #9,22

            y = sign_start.split(",")
            #print("Beginning date = "+y)
            start_month = y[0]
            sign_day = y[1]
            query = "SELECT * FROM \"birthdays\" WHERE b_month = :start_month AND b_day BETWEEN :sign_day AND 31 ORDER BY b_date ASC"
            rows = db.execute(query, start_month=start_month, sign_day=sign_day)

            z = sign_end.split(",")
            end_month = z[0]
            sign_day = z[1]
            query = "SELECT * FROM \"birthdays\" WHERE b_month = :end_month AND b_day BETWEEN 1 AND :sign_day ORDER BY b_date ASC"
            rows2 = db.execute(query,end_month=end_month, sign_day=sign_day)

            rows.extend(rows2) #Combine 2 lists into 1!
        else:
            sign = c_sign
            query = "SELECT * FROM \"birthdays\" WHERE b_year % 12 = CAST(:sign AS int) ORDER BY b_year DESC"
            rows = db.execute(query, sign=sign)

        return render_template("signs.html", z_type=z_type, sign=z_name, rows=rows)