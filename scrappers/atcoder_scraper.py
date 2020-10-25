import requests


def profile_details(username):
    url = "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + str(username)
    try:
        response = requests.get(url)
        data = response.json()
        solve_list = [submission["problem_id"] for submission in data if submission["result"] == "AC"]
        return list(set(solve_list))
    except:
        return []
