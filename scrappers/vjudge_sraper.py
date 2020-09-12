import requests


def profile_details(username):
    url = "https://vjudge.net/user/solveDetail/" + username
    response = requests.get(url)
    data = response.json()
    return data["acRecords"] if "acRecords" in data else {}


def solve_details_in_contest(contest_id, username="", user_id=""):
    url = "https://vjudge.net/contest/rank/single/" + contest_id
    response = requests.get(url)
    data = response.json()
    if user_id == "":
        user_id = get_user_id(data, username)
    if not user_id:
        return 0
    return get_total_solve_in_contest(data, user_id)


def get_contest_name(contest_id):
    url = "https://vjudge.net/contest/rank/single/" + contest_id
    response = requests.get(url)
    data = response.json()
    if "title" not in data or data["title"] is None:
        return "ERROR! Contest not found"
    return data["title"]


def get_total_solve_in_contest(data, user_id):
    solve_set = set()
    user_id = int(user_id)
    if "submissions" not in data:
        return 0
    for submission in data["submissions"]:
        if submission[0] == user_id and submission[2] == 1:
            solve_set.add(submission[1])
    return len(solve_set)


def get_user_id(data, username):
    if username == "" or "participants" not in data:
        return None
    for user_id in data["participants"]:
        if data["participants"][user_id][0] == username:
            return user_id
    return None


if __name__ == '__main__':
    print(solve_details_in_contest(contest_id="393716", username="toufique525", user_id=""))
    data = profile_details("aminul1")
    print(data)
