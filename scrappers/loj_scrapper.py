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
    return sub_list


def save_as_csv(sub_list, name):
    solves_set = set(sub_list)
    output_list = [["Problem", "Solved"]]
    for i in range(1000, 1435):
        output_list.append([i, 1 if i in solves_set else 0])

    with open("output/loj_" + name + ".csv", "w+", newline='') as my_csv:
        csv_writer = csv.writer(my_csv, delimiter=',')
        csv_writer.writerows(output_list)


def save_as_csv_all(list):
    with open("output/loj_solves.csv", "w+", newline='') as my_csv:
        csv_writer = csv.writer(my_csv, delimiter=',')
        csv_writer.writerows(list)


def main():
    session = get_session()
    user_id = ["56751",
               "61043",
               "25347",
               "61569",
               "52870",
               "45559",
               "47787",
               "42920",
               "23609",
               "61991",
               "54363"]
    names = ["Jaber_Al_Siam",
             "BM_Monjur_Morshed",
             "Akash_Lanard",
             "Hasnat_Alam",
             "Ferdous_Islam",
             "Ashik_Iqbal",
             "Sudipta",
             "Sakib_Alamin",
             "Guru_Ananda",
             "Fahid_Shadman_Karim",
             "Salman_Meem_Sahel"]

    solve_list = []
    for user in user_id:
        solve_data = scrape_submission(session, user)
        solve_list.append(solve_data)
        print(user, len(solve_list),len(solve_data))

    output = [["problem_id"]]
    for user in names:
        output[0].append(user)

    for i in range(1000, 1435):
        temp = [i]
        for j in range(len(solve_list)):
            temp.append(1 if i in solve_list[j] else 0)
        output.append(temp)

    save_as_csv_all(output)


def profile_details(user_id):
    try:
        session = get_session()
        return scrape_submission(session, user_id)
    except:
        return []


if __name__ == '__main__':
    main()
