
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, url_for, render_template, redirect
from string import Template

app = Flask(__name__)
app.config["DEBUG"] = True

HTML_TEMPLATE = Template('''
<html>
    <head>
      <title>Tinu's covid-19 statistics</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </head>
    <body>

        <div class="container-fluid">

            <div class="jumbotron text-center">
                <h3>Total-overview in relation to the Swiss population</h3>
            </div>
            <div class="text-center">
                <img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-sum-overview.png" />
            </div>

            <div class="jumbotron text-center">
                <h3>Average-overview in relation to the number of days</h3>
            </div>
            <div class="text-center">
                <img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-avg-overview.png" />
            </div>

            <div class="jumbotron text-center">
                <h3>Dayli overview</h3>
            </div>
            <div class="text-center">
                <img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-cases.png" />
                <br><br>
                <img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-newcases.png" />
                <br><br>
                <img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-host-dead.png" />
            </div>

        </div>

    </body>
</html>
''')

@app.route('/')
def index():
    return render_template("main_page.html")

@app.route('/charts')
def images_page():
    return(HTML_TEMPLATE.substitute())

@app.route('/test')
def test_page():
    images = "<img src=" + url_for("static",filename="images/covid-dayli-cases.png") + "><img src=" + url_for("static",filename="images/covid-dayli-newcases.png") + "><img src=" + url_for("static",filename="images/covid-dayli-host-dead.png") + ">"
    return images

@app.route('/file')
def test_image():
    return redirect(url_for('static', filename='images/covid-dayli-cases.png'), code=301)
