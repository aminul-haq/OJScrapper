import requests


def profile_details(handle):
    try:
        url = "https://codeforces.com/api/user.status?handle=" + handle
        response = requests.get(url)
        data = response.json()
        return reformat_accepted_solve_data(data)
    except:
        return []


def reformat_accepted_solve_data(data):
    if not data or "status" not in data or data["status"] != "OK":
        return []
    data = list(filter(lambda sub: sub["verdict"] == 'OK', data["result"]))
    solve_set = set()
    for submission in data:
        if "problem" in submission:
            problem_id = str(submission["problem"]["contestId"]) + submission["problem"]["index"]
            solve_set.add(problem_id)
    return list(solve_set)


def test():
    handle = "aminul"
    data = profile_details(handle)
    print(data)


if __name__ == '__main__':
    test()
