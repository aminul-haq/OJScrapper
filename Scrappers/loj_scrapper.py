# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import pandas as pd

USERNAME = "askinimran@gmail.com"
PASSWORD = "rcqene5i"

LOGIN_URL = "http://108.161.128.53/login_main.php"
DASHBOARD_URL = "http://108.161.128.53/index.php"


def getSession():
    session = requests.Session()
    response = session.get("http://lightoj.com/login_main.php")
    print(response)
    cookies = session.cookies.get_dict()
    session.post("http://lightoj.com/login_check.php",
                 data={"myuserid": USERNAME,
                       "mypassword": PASSWORD,
                       "Submit": "Login"},
                 headers={"Cookie": "PHPSESSID=" + cookies["PHPSESSID"]})
    return session


def scrape_submission(session, user_id):
    response = session.get("http://lightoj.com/volume_userstat.php?user_id=%s" % user_id)
    soup = BeautifulSoup(response.text, "html.parser")
    submission_table = soup.find_all("table")[6]
    tables = pd.read_html(str(submission_table))
    sub_list = []
    for row in tables:
        for x in row.values.tolist():
            sub_list.extend([int(s) for s in str(x).split() if s.isdigit()])
    print(sub_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    session = getSession()
    user_id = "42920"
    scrape_submission(session, user_id)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
