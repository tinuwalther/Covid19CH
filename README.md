# Covid19CH

This is my Pyhton-project for analysis the covid19-data of Switzerland.

## My challenges

- How can I retrieve the data from the FOPH?
- How can I visualize the data from the FOPH?
- How can I create a history of the data from the FOPH?
- How can I create a chart with the history?
- How can I send the daily data to a messenger?
- Which free messenger can I use?
- Who offers a free way to process data online with Python?
- How can I schedule a Python-script online, create a history and generate charts from this history and present it?

## My learnings

- I had to learn Python
- I had to learn Discord and it's API
- I had to learn the API of FOPH
- I had to learn some DBAs (MSSQL, MongoDB, MySQL)
- I had to learn Pythonanywhere (Scripts, Schedluer, MySQL, Web app)

## My solution

My solution is hosted on [pythonanywhere.com](https://www.pythonanywhere.com/) and use [Discord](https://discord.com/) as messenger.

### Five steps

Create an account on Discord and configure a Webhook.  
Create a beginner account on [pythonanywhere.com](https://www.pythonanywhere.com/).  
Create a scheduler who run my Python-script dayli.   
Create a mysql-database.  
Create a Web app.  

### Python script

My Python-script queries the API of FOPH for the dayli newl laboratory-⁠confirmed cases, laboratory-⁠confirmed hospitalisations and laboratory-⁠confirmed deaths. It saves the result into the mysql-database. My Python-script sends also an message to discord with this data. The script creates three charts of the data based on the mysql-database and save it to the Web app.

### Scheduled Tasks

The beginner account can create one scheduler. The scheduler expire every four weeks, but it can be extended!

The scheduler can run dayli for a beginner account and can schedule Python-scripts to run. And it will be run using the scheduler's default Python version (currrently Python 2.7), to change this behavior add _python3.8 /home/myusername/myproject/myscript.py_ in the task page.

### Mysql database

There is one database with one table, where the dayli cases are stored.

### Web app

The beginner account can create one Web app _your-username.pythonanywhere.com_. This Web app expire after 3 month, to keep it running, you'll need to log in at least once every three months and click the "Run until 3 months from today" button!

There is one flask-based web app hosted on the beginner account, this app only display the two charts with the covid-statistics of Switzerland.

View the web app [tinuwalther.pythonanywhere.com](https://tinuwalther.pythonanywhere.com/).

## Current reports

The fluctuations in the graphics come from late registrations or from the weekends.
Because the FOPH publishes data only from Monday to Friday.

### Overall

![Overview](https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-cases.png)

### Hospitalisations and deaths

![Overview](https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-host-dead.png)

Source: [Federal Office of Public Health FOPH | Bundesamt für Gesundheit BAG](https://www.covid19.admin.ch/en/overview?ovTime=total)