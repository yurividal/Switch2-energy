import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
#import chromedriver_binary     ## enable this to run on windows
from bs4 import BeautifulSoup
import time
import datetime
from influxdb import InfluxDBClient
from dateutil.parser import parse

######### SWITCH2.CO.UK CREDENTIALS ###################
username = ''
pwd = ''

########### GET ALL THE DATA (FIRST RUN) OR GET ONLY THE LATEST DATA (FOR DAILY POLLING)
get = "latest"  # "latest" or all"


########### InfluxDB information. In case you want to save data to influx to grapf with Grafana #############
write_to_influx = True
influxdb_ip = ''
influxdb_port = ''
influxdb_username = ''
influxdb_password = ''
influxdb_database = ''


def writetoinflux(type, date, measurement):
    if (write_to_influx):
        client = InfluxDBClient(host=influxdb_ip, port=influxdb_port,
                                username=influxdb_username, password=influxdb_password)
        client.switch_database(influxdb_database)
        json_body = [
            {
                "measurement": "Switch2",
                "tags": {
                    "type": type
                },
                "time": date,
                "fields": {
                    "measurement": measurement
                }
            }
        ]
        client.write_points(json_body)


options = Options()
options.headless = True
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)
driver.get('https://my.switch2.co.uk/Login')
user = driver.find_element_by_name("UserName")
user.clear()
user.send_keys(username)
print("sending username:  " + username)
driver.find_element_by_id("loginButton").click()
time.sleep(3)
password = driver.find_element_by_id("Password")
password.clear()
print("sending password:  " + pwd)
password.send_keys(pwd)
driver.find_element_by_id("nextStepButton").click()
time.sleep(3)
if ("Welcome" in driver.page_source):
    print("login successfull")

else:
    print("login error")
    return 1

driver.get('https://my.switch2.co.uk/MeterReadings/History')

types = ["Water", "Electricity", "Heat"]

for each_type in types:
    print("#######################  Measurements for " +
          each_type + " ##################################")
    el = driver.find_element_by_id('RegisterId')
    for option in el.find_elements_by_tag_name('option'):
        if each_type in option.text:
            option.click()
            break
    el = driver.find_element_by_id('PageSize')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'All':
            option.click()
            break
    driver.find_element_by_id("ReloadButton").click()

    if (get == "all"):
        for row in driver.find_elements_by_class_name("meter-reading-history-table-data-row"):
            try:
                date = row.find_elements_by_class_name(
                    "meter-reading-history-table-data-row-item")[0]
                try:
                    measurement = row.find_elements_by_class_name(
                        "meter-reading-history-table-data-row-item-right")[0]
                except:
                    measurement = ""

                measurement_int = measurement.text.replace(
                    ' m3', "").replace(' kWh', "")
                print(str(parse(date.text)) + " = " + measurement_int)
                writetoinflux(each_type, parse(
                    date.text), int(measurement_int))
            except:
                pass

    if (get == "latest"):
        driver.find_elements_by_class_name(
            "meter-reading-history-table-data-row")[0]
        try:
            date = driver.find_elements_by_class_name(
                "meter-reading-history-table-data-row-item")[0]
            try:
                measurement = driver.find_elements_by_class_name(
                    "meter-reading-history-table-data-row-item-right")[0]
            except:
                measurement = ""

            measurement_int = measurement.text.replace(
                ' m3', "").replace(' kWh', "")
            print(str(parse(date.text)) + " = " + measurement_int)
            writetoinflux(each_type, parse(date.text), int(measurement_int))
        except:
            pass

driver.quit()
return 0
