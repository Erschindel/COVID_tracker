import math
import datetime as dt

import requests
import numpy as np
import pandas as pd


COVID_URL = "https://api.covid19api.com/summary"

def truncate(number, decimals=3):
    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

try :
    res = requests.get(COVID_URL)
    data = res.json()
except :
    print("No bueno, COVID-19 api failed")

global_pop = 7800000000

# get information from API
global_new_confirmed = data["Global"]["NewConfirmed"]
global_new_total = data["Global"]["TotalConfirmed"]
global_new_deaths = data["Global"]["NewDeaths"]
global_total_deaths = data["Global"]["TotalDeaths"]
global_new_recoveries = data["Global"]["NewRecovered"]
global_total_recoveries = data["Global"]["TotalRecovered"]

global_percentage_increase = 100 * global_new_confirmed / global_new_total

US_data = data["Countries"][177]
US_new_confirmed = US_data["NewConfirmed"]
US_new_total = US_data["TotalConfirmed"]
US_new_deaths = US_data["NewDeaths"]
US_total_deaths = US_data["TotalDeaths"]
US_percentage_increase = 100 * US_new_confirmed / US_new_total

country_list = [data["Countries"][i]["Country"] for i in range(len(data["Countries"]))]

# identify country with highest new cases / total cases
highest_percent_increase_country = ""
list_index = 0
country_percent_increase = 0
for i in range(len(data["Countries"])) :
    percent_increase = (data["Countries"][i]["NewConfirmed"]) / (data["Countries"][i]["TotalConfirmed"])
    if percent_increase > country_percent_increase :
        highest_percent_increase_country = data["Countries"][i]["Country"]
        country_percent_increase = percent_increase
        list_index = i

# print out headline results
print(f"\n---GLOBAL---\nNew confirmed: {global_new_confirmed}\nTotal confirmed: {global_new_total}\nPercentage change: {truncate(global_percentage_increase)}%\n")
print(f"---US---\nNew confirmed: {US_new_confirmed}\nTotal confirmed: {US_new_total}\nPercentage change: {truncate(US_percentage_increase)}%\nPercentage of global: {truncate(100 * US_new_confirmed / global_new_confirmed)}%\n")
print(f"---WORST---\nCountry: {highest_percent_increase_country}\nPercent change: {truncate(100 * country_percent_increase)}%")

population_data = pd.read_csv("data/world_population_data.csv")
US_pop = population_data["2019"][249]
# print(f"\nUS total deaths: {US_total_deaths}\nUS total death per population percentage: {truncate(100 * US_total_deaths / US_pop)}%")

today = dt.datetime.now().date()
today_ser = pd.Series(today, name="date")
each_country_percent_change = pd.Series([100 * (data["Countries"][i]["NewConfirmed"]) / (data["Countries"][i]["TotalConfirmed"]) for i in range(len(data["Countries"]))], name=f"{today}")

new_results_line = today_ser.append(each_country_percent_change)

# print(results.iloc[10:])

# add new data to results.csv
def updateResults () :
    df = pd.read_csv("data/results.csv")
    df = df.append(new_results_line, ignore_index=False)
    df.to_csv("data/results.csv")

    # with open('data/results.csv', 'a') as fd :
        # if today == results.iloc[0:,0] :
        #     print("Today's data has already been entered")
        # else:
        # fd = fd.append(new_results_line)
