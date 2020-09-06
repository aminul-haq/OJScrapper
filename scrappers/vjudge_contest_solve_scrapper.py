# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import time
import datetime
from bs4 import BeautifulSoup
import csv
import json

url_format = "https://vjudge.net/status/data/?start=%d&length=20&res=1&inContest=true&contestId=%s"
url_contest_info = "https://vjudge.net/contest/rank/single/%s"


# url = "https://vjudge.net/status/data/?start=0&length=20&res=1&inContest=true&contestId=389090"


def scrape_data(contest_id, users_map, output_list, total_solve):
    solve_map = get_solve_map(contest_id)
    contest_name = get_contest_name(contest_id)
    output_list[0].append(contest_name)
    for user in users_map:
        user = user.rstrip()
        solves = 0
        if user in solve_map:
            solves = len(solve_map[user])
        id = users_map[user]
        output_list[id].append(solves)
        total_solve[id] = total_solve[id] + solves


def get_contest_name(contest_id):
    url = url_contest_info % (contest_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    contest_data = json.loads(soup.text)
    if "title" not in contest_data or contest_data["title"] is None:
        return "ERROR! Contest not found"
    return contest_data["title"]


def get_solve_map(contest_id):
    map = {}
    time = 0
    while True:
        url = url_format % (time, contest_id)
        time = time + 20
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        submission_data = json.loads(soup.text)
        if "data" not in submission_data or submission_data["data"] is None or len(submission_data["data"]) == 0:
            break
        if "data" in submission_data:
            for data in submission_data["data"]:
                if "statusCanonical" in data and data["statusCanonical"] == "AC":
                    try:
                        # (data["userName"], data["contestNum"])
                        user = data["userName"]
                        problem = data["contestNum"]
                        if user not in map:
                            map[user] = set()
                        map[user].add(problem)

                    except:
                        continue
    return map


def get_handles_list():
    handles = ["sarwar_khalid", "Pharaoh28", "arfaqur", "abdullah_mahmud7", "FairoozR", "necromancer", "bashem",
               "Wasi00007", "trk111", "NadmanKhan", "Moumi_", "toufique525", "2011046642_Opy", "vedistaan",
               "TaneemAhmed", "maxim_v2", "Fahimmanowar", "Junayed_Hasan", "maruf22", "Jushraf", "RifatXia",
               "Rejuana", "omi_farhan75", "OmarHaroon", "Tajreean_Ahmed", "Tayeb183", "Simanta_Mostafa", "MaishaAmin",
               "arman39", "Lamia_Munira", "Ahamed_TJ", "ripcode", "Sunjaree", "ms166", "Antony_Wu"]
    return handles


def get_handles_map():
    map = {}
    id = 1
    for user in get_handles_list():
        map[user] = id
        id = id + 1
    return map


def get_contest_list():
    contest_list = ["372404", "372405", "378225", "378794", "379026", "379283", "379286", "380051", "380795", "381124",
                    "382198", "382422", "383685", "384879", "384978", "387764", "388040", "389090", "388035", "388036",
                    "390274", "391153", "392483"]
    # contest_list = ["389090"]
    return contest_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handles_list = get_handles_list()
    handles_map = get_handles_map()
    contest_list = get_contest_list()
    output_list = [["Username"]]
    total_solve = [0] * (len(handles_list) + 1)
    for user in handles_list:
        output_list.append([user])
    print(output_list)
    for contest_id in contest_list:
        scrape_data(contest_id, handles_map, output_list, total_solve)
        print("done contest", contest_id)

    output_list[0].append("Total Solve")
    for i in range(1, len(total_solve)):
        output_list[i].append(total_solve[i])

    print(output_list)

    with open("output/rank_list_" + datetime.datetime.today().strftime("%d-%m-%Y") + ".csv", "w+",
              newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(output_list)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
