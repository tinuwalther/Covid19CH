# Covid19CH

This is my Pyhton-project for analysis covid19-data of Switzerland.

## My challenges

- How can I retrieve the data from the FOPH?
- How can I visualize the data from the FOPH?
- How can I create a history of the data from the FOPH?
- How can I create a chart with the history?
- How can I send the daily data to a messenger?
- Which free messenger can I use?
- Who offers a free way to process data online with Python?
- How can I schedule a Python script online, create a history and generate charts from this history and present it?

## My learnings

- I had to learn Python
- I had to learn Discord and it's API
- I had to learn the API of FOPH
- I had to learn some DBAs (MSSQL, MongoDB, MySQL)
- I had to learn Pythonanywhere (Scripts, Schedluer, MySQL, Website)

## My solution

My solution is hosted on [pythonanywhere.com](https://www.pythonanywhere.com/) and use [Discord](https://discord.com/) as messenger.

### Five steps

Create an account on Discord and configure a Webhook.
Create a beginner account on [pythonanywhere.com](https://www.pythonanywhere.com/) to schedule a python-script, 
create a mysql-database, 
and create a website on your account.

### Python script

The Python script scrapp the API for the dayli newl laboratory-⁠confirmed cases, laboratory-⁠confirmed hospitalisations and laboratory-⁠confirmed deaths and save it into the mysql-database. This script sends also an message to discord with this data.
The script creates two charts of the data based on the mysql-database and save it to the website.

### Scheduled Tasks

The scheduler in pythonanywhere.com can run dayli for a beginner account and can schedule Python scripts to run.

### Mysql database

There is one database with one table, where the dayli cases are stored.

### Website

There is one flask-based web app hosted on the beginner account, this app only display the two charts with the covid-statistics of Switzerland.

## Current reports

The fluctuations in the graphics come from late registrations or from the weekends.
Because the FOPH publishes data only from Monday to Friday.

### Overall

![Overview](https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-cases.png)

### Only new cases

![Overview](https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-newcases.png)

### Hospitalisations and deaths

![Overview](https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-host-dead.png)

Source: [Federal Office of Public Health FOPH | Bundesamt für Gesundheit BAG](https://www.covid19.admin.ch/en/overview?ovTime=total)