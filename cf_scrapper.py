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
    submissions = json.loads(response.text)
    if submissions["status"] != "OK":
        pass
    submissions = list(filter(lambda sub: sub["verdict"] == 'OK', submissions["result"]))
    print(submissions)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handle = "aminul"
    scrape_data(handle)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
