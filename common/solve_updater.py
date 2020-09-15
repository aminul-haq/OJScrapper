from common.database import Database
from models.oj_model import OjModel, COLLECTION_NAME as OJ_COLLECTION_NAME
from models.user_model import UserModel, COLLECTION_NAME as USER_COLLECTION_NAME
from models.student_model import StudentModel, COLLECTION_NAME as BOOTCAMP_COLLECTION_NAME
from models.classroom_model import ClassroomModel
from scrappers.vjudge_sraper import profile_details as vjudge_details, solve_details_in_contest
from scrappers.cf_scrapper import profile_details as cf_details
from scrappers.loj_scrapper import profile_details as loj_details
from scrappers import vjudge_sraper
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


def bootcamp_update_one(username):
    user = UserModel.get_by_username(username)
    classroom = ClassroomModel.get_by_classroom_name(user.classroom_name)
    bootcamp = StudentModel.get_by_username(username)
    if not bootcamp:
        bootcamp = StudentModel(username=username, bootcamp_name=user.classroom_name)
    if not classroom:
        return

    vjudge_handle = OjModel.get_by_username(username).oj_info[VJUDGE][USERNAME]
    long_contests = []
    for contest in classroom.vjudge_contest_list:
        long_contests.append({
            "contest_title": contest["contest_title"],
            "total_problems": contest["total_problems"],
            "minimum_solve_required": contest["minimum_solve_required"],
            "solved_problems": solve_details_in_contest(contest_id=contest["contest_id"], username=vjudge_handle)
        })
    data = {
        "long_contests": long_contests
    }
    print(data)
    bootcamp.update_to_mongo(data)


def bootcamp_update_all():
    user_list = Database.get_all_records("users")
    for user in user_list:
        bootcamp_update_one(user[USERNAME])


def update_students(classroom):
    data_map = {}
    for contest in classroom.vjudge_contest_list:
        data_map[contest["contest_id"]] = vjudge_sraper.get_contest_details_data(contest["contest_id"])
    for username in classroom.user_list:
        vjudge_handle = None
        try:
            vjudge_handle = OjModel.get_by_username(username).oj_info[VJUDGE][USERNAME]
        except:
            continue
        student = StudentModel.get_by_username_and_classroom_name(username, classroom.classroom_name)
        long_contests = []
        for contest in classroom.vjudge_contest_list:
            long_contests.append(
                {
                    "contest_title": contest["contest_title"],
                    "total_problems": contest["total_problems"],
                    "minimum_solve_required": contest["minimum_solve_required"],
                    "solved_problems": vjudge_sraper.solve_details_in_contest_from_data(
                        data=data_map[contest["contest_id"]],
                        username=vjudge_handle),
                    "contest_type": contest["contest_type"]
                }
            )
        new_values = {
            "long_contests": long_contests
        }
        student.update_to_mongo(new_values)


if __name__ == '__main__':
    Database.initialize()
    bootcamp_update_one("bashem")
