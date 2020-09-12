# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
# import time
from bs4 import BeautifulSoup
import csv
import re
import json


def scrape_data(handle):
    url = "https://codeforces.com/api/user.status?handle=" + handle
    response = requests.get(url)
    data = response.json()
    return reformat_accepted_solve_data(data)


def reformat_accepted_solve_data(data):
    data = list(filter(lambda sub: sub["verdict"] == 'OK', data["result"]))
    solve_set = set()
    for submission in data:
        if "problem" in submission:
            problem_id = str(submission["problem"]["contestId"]) + submission["problem"]["index"]
            solve_set.add(problem_id)
    return list(solve_set)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handle = "aminul"
    data = scrape_data(handle)
    print(data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
