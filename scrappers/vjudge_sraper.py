import requests


def profile_details(username):
    try:
        url = "https://vjudge.net/user/solveDetail/" + username
        response = requests.get(url)
        data = response.json()
        return data["acRecords"] if "acRecords" in data else {}
    except:
        return {}


def solve_details_in_contest(contest_id, username="", user_id=""):
    url = "https://vjudge.net/contest/rank/single/" + contest_id
    response = requests.get(url)
    data = response.json()
    if user_id == "":
        user_id = get_user_id(data, username)
    if not user_id:
        return 0
    return get_total_solve_in_contest(data, user_id)


def get_contest_details_data(contest_id):
    url = "https://vjudge.net/contest/rank/single/" + contest_id
    response = requests.get(url)
    data = response.json()
    return data


def get_contest_details_data_formatted(contest_id):
    url = "https://vjudge.net/contest/rank/single/" + contest_id
    response = requests.get(url)
    data = response.json()
    begin_time = data["begin"]

    user_map = {}
    for user_id in data["participants"]:
        user_map[user_id] = data["participants"][user_id][0]

    solve_map = {}
    solve_map_set = {}
    for submission in data["submissions"]:
        if submission[2] == 1:
            username = user_map[str(submission[0])]
            submission_time = begin_time + (submission[len(submission) - 1] * 1000)
            problem_id = submission[1]
            if username not in solve_map:
                solve_map[username] = list()
                solve_map_set[username] = set()
            if problem_id not in solve_map_set[username]:
                solve_map[username].append([problem_id, submission_time])
                solve_map_set[username].add(problem_id)

    for username in solve_map:
        solve_map[username] = sorted(solve_map[username], key=lambda row: row[1], reverse=False)

    return {
        "id": data["id"],
        "title": data["title"],
        "begin": data["begin"],
        "length": data["length"],
        "submission": solve_map
    }


def get_user_id(data, username):
    if username == "" or "participants" not in data:
        return None
    for user_id in data["participants"]:
        if data["participants"][user_id][0] == username:
            return user_id
    return None


def get_contest_name(contest_id):
    url = "https://vjudge.net/contest/rank/single/" + contest_id
    response = requests.get(url)
    data = response.json()
    if "title" not in data or data["title"] is None:
        return "ERROR! Contest not found"
    return data["title"]


def get_contest_name_from_data(data):
    if "title" not in data or data["title"] is None:
        return "ERROR! Contest not found"
    return data["title"]


def solve_details_in_contest_from_data(data, username="", user_id=""):
    if user_id == "":
        user_id = get_user_id(data, username)
    if not user_id:
        return 0
    return get_total_solve_in_contest(data, user_id)


def get_total_solve_in_contest(data, user_id):
    solve_set = set()
    user_id = int(user_id)
    if "submissions" not in data:
        return 0
    for submission in data["submissions"]:
        if submission[0] == user_id and submission[2] == 1:
            solve_set.add(submission[1])
    return len(solve_set)


def solve_details_in_contest_from_data_with_timestamp(data, start_time, end_time, username="", user_id=""):
    if user_id == "":
        user_id = get_user_id(data, username)
    if not user_id:
        return 0
    return get_total_solve_in_contest_with_timestamp(data, user_id, start_time, end_time)


def get_total_solve_in_contest_with_timestamp(data, user_id, start_time, end_time):
    solve_set = set()
    user_id = int(user_id)
    begin_time = data["begin"]
    if "submissions" not in data:
        return 0
    for submission in data["submissions"]:
        submission_time = begin_time + (submission[len(submission) - 1] * 1000)
        if submission_time < start_time or submission_time > end_time:
            continue
        if submission[0] == user_id and submission[2] == 1:
            solve_set.add(submission[1])
    return len(solve_set)


def main():
    # print(solve_details_in_contest(contest_id="393716", username="toufique525", user_id=""))
    # data = profile_details("aminul1")
    # print(data)
    data = get_contest_details_data_formatted("389090")
    print(data)


if __name__ == '__main__':
    main()
