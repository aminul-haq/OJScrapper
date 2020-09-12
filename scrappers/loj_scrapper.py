import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

USERNAME = "askinimran@gmail.com"
PASSWORD = "rcqene5i"

LOGIN_URL = "http://108.161.128.53/login_main.php"
DASHBOARD_URL = "http://108.161.128.53/index.php"


def get_session():
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


def save_as_csv(sub_list, user_id):
    solves_set = set(sub_list)
    output_list = [["Problem", "Solved"]]
    for i in range(1000, 1435):
        output_list.append([i, i in solves_set])

    with open("output/loj_" + user_id + ".csv", "w+", newline='') as my_csv:
        csv_writer = csv.writer(my_csv, delimiter=',')
        csv_writer.writerows(output_list)


def main():
    session = get_session()
    user_id = "25347"
    scrape_submission(session, user_id)


if __name__ == '__main__':
    main()
