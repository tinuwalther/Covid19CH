# coding=utf-8
import requests
import MySQLdb, sys, os, json, re
import pandas as pd

from datetime import datetime

# MySQL
def validate_string(val):
    '''Do validation and checks before insert'''
    if val != None:
        if type(val) is int:
            return str(val).encode('utf-8')
        else:
            return val

def get_table(sqlconnection, table, output = False):
    '''Test table exists'''
    sql = "SHOW TABLES LIKE '%s' "% ('%'+str(table)+'%')
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if output:
            print("[INFO]\t{0}():\tTable {1} = {2}".format(sys._getframe().f_code.co_name, table, result[0]))
    except Exception as e:
        print("[WARN]\t{0}():\t{1}\t{2}".format(sys._getframe().f_code.co_name, table, e))
        result = False

    return result

def drop_table(sqlconnection, table, output = False):
    '''Dropping table if already exists'''
    sql = "DROP TABLE IF EXISTS " + table
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        if output:
            print("[INFO]\t{0}():\tTable {1} dropped".format(sys._getframe().f_code.co_name, table))
        return True
    except Exception as e:
        print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))
        return False

def create_table(sqlconnection, table, tabledefinition, output = False):
    '''Creating table'''
    sql = "CREATE TABLE " + table + "(" + tabledefinition + ")"
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        if output:
            print("[INFO]\t{0}():\tTable {1} created".format(sys._getframe().f_code.co_name, table))
        return True
    except Exception as e:
        print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))
        return False

def get_rows(sqlconnection, table, output = False):
    '''Get all rows from table'''
    sql = "SELECT * FROM %s"% (str(table))
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if output:
            print("[INFO]\t{0}():\tTable {1} = {2}".format(sys._getframe().f_code.co_name, table, result[0]))
    except Exception as e:
        print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))

    return result

def insert_into(sqlconnection, table, date, cases, hosp, death, output = False):
    '''Insert one record'''
    errorcount = 0
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(
            "INSERT INTO " + table + " (date, cases, hosp, death) VALUES (%s,%s,%s,%s)", (date, cases, hosp, death)
        )
        sqlconnection.commit()
        if output:
            print("[INFO]\t{0}():\tRecord inserted into table {1}".format(sys._getframe().f_code.co_name, table))
        return True
    except Exception as e:
        print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))
        errorcount + 1
        return False

def import_json(json_file, sqlconnection, table, droptable = False):
    '''Import data from JSON-file'''
    check_path = os.path.exists(json_file)
    if(check_path == True):

        # Read JSON file
        json_data = open(json_file).read()
        json_obj  = json.loads(json_data)

        if droptable:
            if drop_table(sqlconnection, table, output = True):
                create_table(sqlconnection, table, "date VARCHAR(10) NOT NULL, cases INT, hosp INT, death INT", output = True)

        # parse json data to SQL insert
        errorcount   = 0
        successcount = 0
        for i, item in enumerate(json_obj):
            date  = validate_string(item.get("Datum", None))
            cases = int(validate_string(item.get("Neue Fälle", None)))
            hosp  = int(validate_string(item.get("Hospitalisationen", None)))
            death = int(validate_string(item.get("Todesfälle", None)))

            try:
                result = insert_into(sqlconnection, mytable, date, cases, hosp, death)
                if result:
                    successcount = successcount + 1
                else:
                    errorcount   = errorcount + 1
            except Exception as e:
                print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))
                errorcount + 1

        print("[INFO]\t{0}():\tInserted {1} records with {2} errors".format(sys._getframe().f_code.co_name, successcount ,errorcount))

def save_linechart(data, x, y, title, path, output = False):
    '''Create chart and save it to downloads'''
    chart = data.plot.line(
        x       = x,
        xlabel  = "",
        ylabel  = "",
        y       = y,
        title   = title,
        grid    = True,
        legend  = True,
        figsize = (15,5)
    )
    ### Save chart as png-file
    fig = chart.get_figure()
    fig.savefig(path, facecolor='w', bbox_inches='tight')
    try:
        if os.path.exists(path):
            if output:
                print("[INFO]\t{0}():\tChart saved as {1}".format(sys._getframe().f_code.co_name, path))
        else:
            if output:
                print("[INFO]\t{0}():\tCould not save chart as {1}".format(sys._getframe().f_code.co_name, path))
    except Exception as e:
        print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))


def save_sumchart(data, title, path, output = False):
    '''Create chart and save it to downloads'''

    ### Calculate sum of values
    sum_of_swiss_people  = 8655118
    sum_of_new_cases     = int(sum(data.Cases))
    sum_of_new_hosp      = int(sum(data.Hosp))
    sum_of_new_dead      = int(sum(data.Death))

    ### Calculate percent of values
    pct_swiss_people     = "{:.2%}".format(1)
    pct_new_cases        = "{:.2%}".format(sum_of_new_cases / sum_of_swiss_people)
    pct_new_hosp         = "{:.2%}".format(sum_of_new_hosp  / sum_of_swiss_people)
    pct_new_dead         = "{:.2%}".format(sum_of_new_dead  / sum_of_swiss_people)

    ### Create the dictionary
    sum_pie_dict = {
        'Summe'  :[sum_of_swiss_people,sum_of_new_cases,sum_of_new_hosp,sum_of_new_dead],
        'Percent':[pct_swiss_people,pct_new_cases,pct_new_hosp,pct_new_dead]
    }

    ### Create the data frame set
    sum_pie_df = pd.DataFrame(data=sum_pie_dict)
    pie_index  = [
        f'Total swiss people: {sum_of_swiss_people}',
        f'Total cases: {sum_of_new_cases}',
        f'Total hospitalisations: {sum_of_new_hosp}',
        f'Total deaths: {sum_of_new_dead}'
    ]

    ### Print out the pie cahrt
    sum_plot_colors = ['lightgreen', 'yellow', 'orange', 'red']
    sum_pie_explode = (0,0.3,0.6,2.5)
    pie = sum_pie_df.plot.pie(
        title   = title,
        labels  = pie_index,
        legend  = True,
        ylabel  = "", y = 'Summe',
        autopct = '%1.2f%%',
        #table   = True,
        colors  = sum_plot_colors,
        explode = sum_pie_explode,
        figsize = (20,5),
    )

    ### Save chart as png-file
    fig = pie.get_figure()
    fig.savefig(f'{path}', facecolor='w', bbox_inches='tight')

    try:
        if os.path.exists(path):
            if output:
                print('[INFO]\t{0}():\tChart saved as {1}'.format(sys._getframe().f_code.co_name, path))
        else:
            if output:
                print('[INFO]\t{0}():\tCould not save chart as {1}'.format(sys._getframe().f_code.co_name, path))
    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))


def save_avgchart(data, title, path, output = False):
    '''Create chart and save it to downloads'''

    ### Calculate sum of values
    sum_of_new_cases     = int(sum(data.Cases))
    sum_of_new_hosp      = int(sum(data.Hosp))
    sum_of_new_dead      = int(sum(data.Death))

    ## Build average of data
    count_of_datum   = data.Date.count()
    avg_of_new_cases = int(sum_of_new_cases / count_of_datum)
    avg_of_new_hosp  = int(sum_of_new_hosp / count_of_datum)
    avg_of_new_dead  = int(sum_of_new_dead / count_of_datum)

    ## Create the dictionary with avg and sum
    pie_index   = [
        f'Average cases: {avg_of_new_cases}',
        f'Average hospitalisations: {avg_of_new_hosp}',
        f'Average deaths: {avg_of_new_dead}'
    ]

    pie_dict = {
        'Average':[avg_of_new_cases,avg_of_new_hosp,avg_of_new_dead],
        'Summe'  :[sum_of_new_cases,sum_of_new_hosp,sum_of_new_dead],
    }

    ### Print out the pie cahrt
    plot_colors    = ['lightblue', 'orange','red']
    avg_pie_df = pd.DataFrame(data = pie_dict)
    avg_pie_explode = (0,0.6,1.4)
    pie = avg_pie_df.plot.pie(
        #subplots = True,
        ylabel  = "", y = 'Average',
        title   = title,
        labels  = pie_index,
        #table   = True,
        autopct = '%1.2f%%',
        colors  = plot_colors,
        explode = avg_pie_explode,
        figsize = (20,5)
    )

    ### Save chart as png-file
    fig = pie.get_figure()
    fig.savefig(f'{path}', facecolor='w', bbox_inches='tight')

    try:
        if os.path.exists(path):
            if output:
                print('[INFO]\t{0}():\tChart saved as {1}'.format(sys._getframe().f_code.co_name, path))
        else:
            if output:
                print('[INFO]\t{0}():\tCould not save chart as {1}'.format(sys._getframe().f_code.co_name, path))
    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))


# Discord
def send_discord_message(data, date):
    '''Send Discord message'''
    webhook_url         = 'https://discordapp.com/api/webhooks/851028735331008512/JCYUCmlSfAm_Cl0d6mQxyx45RXZae1xR-OU0FIRA8hp1hoMNQzlHx8dHcVSiKeTjB4Fb' #'your webhook address'
    author_name         = 'Covid19 Hook'
    author_avatar       = 'https://i2.pngguru.com/preview/189/787/605/covid19-coronavirus-corona-violet-pink-purple-cartoon-magenta-smile-png-clipart-thumbnail.jpg'
    section_title       = '[INFO] COVID-19 Statistics for SWITZERLAND'
    section_description = "Information on the current situation, as of " + date

    embeds = {
        "title": section_title, "description": section_description, "color": 32767,
        "fields": [
            {"name" : "Confirmed Cases", "value" : data["Cases"], "inline": "true"},
            {"name" : "Hospitalisations", "value" : data["Hospitalisations"], "inline": "true"},
            {"name" : "Deaths", "value" : data["Deaths"], "inline": "true"},
            {"name" : "Covid19 charts", "value" : "[Tinu's covid19 charts on pythonanywhere.com](https://tinuwalther.pythonanywhere.com/)"},
            {"name" : "Official website", "value" : "[Federal Office of Public Health FOPH | Bundesamt für Gesundheit BAG](https://www.covid19.admin.ch/en/overview?ovTime=total)"}
        ]
    }

    data = {
        "username": author_name, "avatar_url": author_avatar, "embeds": [embeds],
    }

    headers = {
        "Content-Type": "application/json"
    }

    result = requests.post(webhook_url, json=data, headers=headers)
    if 200 <= result.status_code < 300:
        print("[INFO]\t{0}():\tWebhook sent {1}".format(sys._getframe().f_code.co_name, result.status_code))
    else:
        print("[WARN]\t{0}():\tNot sent with {1}, response: {2}".format(sys._getframe().f_code.co_name, result.status_code, result.json()))

# Covid19-CH API
def get_api_context(url):
    '''return JSON-file'''
    from bson.json_util import loads
    response = requests.get(url +"/context")
    if(response.status_code == 200):
        html_content = response.content.decode('utf-8')
        json_data = loads(html_content)
        if "dataVersion" in json_data:
            dataVersion = json_data["dataVersion"]
        else:
            dataVersion = None
            print("dataVersion not found")

        return dataVersion

    else:
        print(response.status_code)

def get_api_data(url, type, last_update):
    '''return JSON'''
    from bson.json_util import loads
    data_json_url = url + "/sources/COVID19" + type + "_geoRegion.json"
    response = requests.get(data_json_url)
    if(response.status_code == 200):
        html_content = response.content.decode("utf-8")
        json_data = loads(html_content)
        for row in json_data:
            if row["geoRegion"] == "CH":
                if row["datum"] == last_update:
                    return "Total:\t" + str(row["sumTotal"]) + "\nToday:\t" + str(row["entries_diff_last"])


if __name__ =="__main__":

    import datetime as dt

    api_url      = "https://www.covid19.admin.ch/api/data"
    data_version = get_api_context(api_url)
    last_update  = data_version[0:4] + "-" + data_version[4:6] + "-" + data_version[6:8]
    dt_format    = "%Y-%m-%d"
    dt_today     = dt.datetime.today()
    str_today    = dt_today.strftime(dt_format)
    dt_weekday   = dt.datetime.strptime(str_today, dt_format).strftime('%A')
    if dt_weekday == 'Saturday' or dt_weekday == 'Sunday':
        #print('Its weekend: ' + dt_weekday)
        pass
    else:
        #print(dt_weekday)
        data_version_url = api_url + "/" + data_version
        if data_version_url:
            cases = get_api_data(data_version_url, "Cases", last_update)
            hosp  = get_api_data(data_version_url, "Hosp", last_update)
            death = get_api_data(data_version_url, "Death", last_update)
            discord_data = {
                "Cases": cases,
                "Hospitalisations": hosp,
                "Deaths": death,
            }
            print(discord_data)

            # Initiate MySQL variables
            sqlhost   = 'your-db-host-address'
            sqluser   = 'your-db-user'
            sqlusrpw  = 'your-db-password'
            mydb      = 'your-db-name'
            mytable   = 'your-db-table'

            # Open database connection
            sqlconnection = MySQLdb.connect(sqlhost,sqluser,sqlusrpw,mydb)

            # Adapt data for MySQL
            dt_last_update   = dt.datetime.strptime(last_update, dt_format)
            dt_format        = "%d.%m.%Y"
            str_last_update  = dt_last_update.strftime(dt_format)
            result           = insert_into(sqlconnection, mytable, str_last_update, int(cases.split("\t")[2]), int(hosp.split("\t")[2]), int(death.split("\t")[2]), output = True)

            if result:
                covid_data = get_rows(sqlconnection, mytable, output = False)

                result_of_history = []
                for row in covid_data:
                    thisdict = {
                        'Date'   : datetime.strptime(row[0], dt_format),
                        'Cases'  : row[1],
                        'Hosp'   : row[2],
                        'Death'  : row[3],
                    }
                    result_of_history.append(thisdict)

                # Create a data frame set and print out as table
                df = pd.DataFrame(result_of_history)
                print(df)

                count_of_datum = df.Date.count()
                first_value    = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(df.Date.values[0]))[0])
                last_value     = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(df.Date.values[count_of_datum -1]))[0])

                # Print data frame set as line chart
                save_linechart(df, "Date", ["Cases","Hosp","Death"], "Laboratory-⁠confirmed cases - as of: " + last_value, "/home/tinuwalther/mysite/static/images/covid-dayli-cases.png", output = True)
                save_linechart(df, "Date", ["Cases"], "Laboratory-⁠confirmed cases - as of: " + last_value, "/home/tinuwalther/mysite/static/images/covid-dayli-newcases.png", output = True)
                save_linechart(df, "Date", ["Hosp","Death"], "Laboratory-⁠confirmed hospitalisations and deaths - as of: " + last_value, "/home/tinuwalther/mysite/static/images/covid-dayli-host-dead.png", output = True)

                # Print data frame set as pie chart
                try:
                    save_sumchart(df, f"Total-overview in relation to the Swiss population since {first_value} - as of: {last_value}", "/home/tinuwalther/mysite/static/images/covid-sum-overview.png", output = True)
                    save_avgchart(df, f"Average-overview in relation to the number of days since {first_value} - as of: {last_value}", "/home/tinuwalther/mysite/static/images/covid-avg-overview.png", output = True)
                except Exception as e:
                    print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))

                # disconnect from server
                sqlconnection.close()

            send_discord_message(discord_data, last_update)
