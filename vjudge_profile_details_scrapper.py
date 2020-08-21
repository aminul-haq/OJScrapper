# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import time
import datetime
from bs4 import BeautifulSoup
import csv
import re
import json

last7DaysKey = "New solved in last 7 days"
last30DaysKey = "New solved in last 30 days"
overall_key = "Overall solved"


def scrape_data(handle):
    url = "https://vjudge.net/user/" + handle
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a = get_solve_count(soup, last7DaysKey)
    b = get_solve_count(soup, last30DaysKey)
    c = get_solve_count(soup, overall_key)
    # print(handle, a, b, c)
    return [handle, a, b, c]


def get_solve_count(soup, key):
    things = soup.find_all(text=True, attrs={"title": key})
    return int(re.split('>|>|<', str(things[0]))[2])


def solve_details(handle):
    url = "https://vjudge.net/user/solveDetail/" + handle
    response = requests.get(url)
    #soup = BeautifulSoup(response.text, "html.parser")
    solve_data = json.loads(response.text)
    print(solve_data)


def get_handles_list():
    handles = ["sarwar_khalid", "Pharaoh28", "arfaqur", "abdullah_mahmud7", "FairoozR", "necromancer", "bashem",
               "Wasi00007", "trk111", "NadmanKhan", "Moumi_", "toufique525", "2011046642_Opy", "vedistaan",
               "TaneemAhmed", "maxim_v2", "Fahimmanowar", "Junayed_Hasan", "maruf22", "Jushraf", "RifatXia",
               "Rejuana", "omi_farhan75", "OmarHaroon", "Tajreean_Ahmed", "Tayeb183", "Simanta_Mostafa", "MaishaAmin",
               "arman39", "Lamia_Munira", "Ahamed_TJ", "ripcode", "Sunjaree", "ms166", "Antony_Wu"]
    return handles


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     solve_list = []
#     # solve_list.append(["Handle", "Last 7 days", "Last 30 days", "Overall solve"])
#     handles = get_handles_list()
#     for user in handles:
#         solve_list.append(scrape_data(user))
#     sorted_list = sorted(solve_list, key=lambda x: (x[2], x[3]), reverse=True)
#     sorted_list.insert(0, ["Handle", "Last 7 days", "Last 30 days", "Overall solve"])
#     # print(sorted_list)
#     with open("rank_list_" + datetime.datetime.today().strftime("%d-%m-%Y") + ".csv", "w+", newline='') as my_csv:
#         csvWriter = csv.writer(my_csv, delimiter=',')
#         csvWriter.writerows(sorted_list)

solve_details("aminul1")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
