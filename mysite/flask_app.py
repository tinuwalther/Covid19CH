
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, url_for, render_template, redirect
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def index():
    '''Render the root page'''
    author_name               = "Martin Walther"

    total_overview_nav_title  = "Total"
    total_overview_title      = "Total overview"
    total_overview_text       = "Total overview in relation to the Swiss population"
    total_overview_chart      = "https://tinuwalther.pythonanywhere.com/static/images/covid-sum-overview.png"

    avg_overview_nav_title    = "Average"
    avg_overview_title        = "Average overview"
    avg_overview_text         = "Average overview in relation to the number of days"
    avg_overview_chart        = "https://tinuwalther.pythonanywhere.com/static/images/covid-avg-overview.png"

    daily_overview_nav_title  = "Daily overview"
    daily_overview_title      = "Daily overview"
    daily_overview_text       = "Daily overview of new cases, hospitalisations and deaths"
    daily_overview_chart      = "https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-cases.png"
    daily_new_text            = "Daily new laboratory-⁠confirmed hospitalisations in relation to deaths"
    daily_new_chart           = "https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-host-dead.png"

    weekly_average_nav_title  = "Weekly average"
    weekly_average_title      = "Weekly average"
    weekly_average_text_all   = "Weekly average of cases, hospitalisations and deaths"
    weekly_average_chart_all  = "https://tinuwalther.pythonanywhere.com/static/images/covid-weekly-avg-overview.png"
    weekly_average_text_spec  = "Weekly average of hospitalisations in relation to deaths"
    weekly_average_chart      = "https://tinuwalther.pythonanywhere.com/static/images/covid-weekly-avg-host-death.png"

    timestamp = datetime.now()

    return render_template("main_page.html", **locals())


@app.route('/test')
def test_page():
    images = "<img src=" + url_for("static",filename="images/covid-dayli-cases.png") + "><img src=" + url_for("static",filename="images/covid-dayli-newcases.png") + "><img src=" + url_for("static",filename="images/covid-dayli-host-dead.png") + ">"
    return images


@app.route('/file')
def test_image():
    return redirect(url_for('static', filename='images/covid-dayli-cases.png'), code=301)
