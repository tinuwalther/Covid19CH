
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
        <meta name="author" content="Martin Walther Foto & IT"/>
        <meta name="keywords" content="Covid, Covid19, Covid-19, Covid-Statistics, Covid-Statistics of Switzerland, Coronavirus, BAG, FOPH, Switzerland, Python" />

        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"  />
        <link href="https://fonts.googleapis.com/css?family=Quicksand&display=swap" rel="stylesheet"  />

        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"  ></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"  ></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"  ></script>

        <style>
            p { margin-top: 1em; }
            p { margin-bottom: 1em; }
        </style

    </head>
    <body>

        <!-- Navbar as a heading -->
        <nav Class="navbar navbar-expand-sm bg-dark navbar-dark sticky-top"  >
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Covid-19 Statistics of Switzerland</a>
                <button Class="navbar-toggler" data-toggle="collapse" type="button" data-target="#collapsibleNavbar"  >
                    <span Class="navbar-toggler-icon"  ></span>
                </button>
                <div Id="collapsibleNavbar" Class="collapse navbar-collapse"  >
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link" href="#sum">Total</a>
                         </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#avg">Average</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#overview">Overview</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#cases">Cases</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#hosp">Hospitalisations</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#hosp">Deaths</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="container-xxl">

            <a id="sum"></a>
            <div class="jumbotron text-center">
                <h3>Total-overview in relation to the Swiss population</h3>
            </div>
            <div class="text-center">
                <span>
                    <p><img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-sum-overview.png" /></p>
                </span>
            </div>

            <a id="avg"></a>
            <div class="jumbotron text-center">
                <h3>Average-overview in relation to the number of days</h3>
            </div>
            <div class="text-center">
                <span>
                    <p><img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-avg-overview.png" /></p>
                </span>
            </div>

            <a id="overview"></a>
            <div class="jumbotron text-center">
                <h3>Dayli overview of new cases, hospitalisations and deaths</h3>
                <hr>
                <p>They have been supplemented with late, incorrect and duplicate reports from the period from March 2020 to June 2021.</p>
            </div>
            <div class="text-center">
                <span>
                    <p><img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-cases.png" /></p>
                </span>
            </div>

            <a id="cases"></a>
            <div class="jumbotron text-center">
                <h3>Dayli new laboratory-⁠confirmed cases</h3>
                <hr>
                <p>They have been supplemented with late, incorrect and duplicate reports from the period from March 2020 to June 2021.</p>
            </div>
            <div class="text-center">
                <span>
                    <p><img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-newcases.png" /></p>
                </span>
            </div>

            <a id="hosp"></a>
            <div class="jumbotron text-center">
                <h3>Dayli new laboratory-⁠confirmed hospitalisations and deaths</h3>
                <hr>
                <p>They have been supplemented with late, incorrect and duplicate reports from the period from March 2020 to June 2021.</p>
            </div>
            <div class="text-center">
                <span>
                    <p><img class="img-fluid" src="https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-host-dead.png" /></p>
                </span>
            </div>

        </div>
        <p>
            <br>
        </p>

        <nav class="navbar fixed-bottom navbar-light bg-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Top</a>Copyright © 2021 Martin Walther
            </div>
        </nav>

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

