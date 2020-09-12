from common.database import Database
from models.oj_model import OjModel, COLLECTION_NAME as OJ_COLLECTION_NAME
from models.user_model import UserModel, COLLECTION_NAME as USER_COLLECTION_NAME
from scrappers.vjudge_sraper import profile_details as vjudge_details
from scrappers.cf_scrapper import profile_details as cf_details
from scrappers.loj_scrapper import profile_details as loj_details
from common.OjMap import *


def update_one(username):
    user = OjModel.get_by_username(username)
    oj_profiles = user.oj_info
    try:
        vjudge_data = vjudge_details(oj_profiles[VJUDGE][USERNAME])
    except:
        vjudge_data = {}
    for oj in vjudge_data:
        if oj not in oj_profiles:
            oj_profiles[oj] = {
                USERNAME: None,
                SOLVE_LIST: vjudge_data[oj]
            }
        else:
            oj_profiles[oj][SOLVE_LIST] = vjudge_data[oj]
        oj_profiles[oj][SOLVE_LIST] = [str(x) for x in oj_profiles[oj][SOLVE_LIST]]  # converting to list of strings

    update_json(oj_profiles, CODEFORCES, cf_details)
    update_json(oj_profiles, LIGHTOJ, loj_details)

    user.update_to_mongo({"oj_info": oj_profiles})


def update_json(oj_profiles, oj_name, arg):
    if oj_name in oj_profiles and oj_profiles[oj_name]:
        solve_list_data = arg(oj_profiles[oj_name][USERNAME])
        solve_list_data = [str(x) for x in solve_list_data]  # converting to list of strings
        if SOLVE_LIST in oj_profiles[oj_name] and oj_profiles[oj_name][SOLVE_LIST]:
            oj_profiles[oj_name][SOLVE_LIST].extend(solve_list_data)
        else:
            oj_profiles[oj_name][SOLVE_LIST] = solve_list_data
        oj_profiles[oj_name][SOLVE_LIST] = list(set(oj_profiles[oj_name][SOLVE_LIST]))


def update_all():
    user_list = Database.get_all_records("users")
    for user in user_list:
        update_one(user[USERNAME])


# if __name__ == '__main__':
#     Database.initialize()
#     update_one("abir")
