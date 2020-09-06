import csv
import json

def solve(file_1, file_2):
    map = {}
    with open(file_1, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row_list = list(row)
            if row_list[0] == "Username":
                continue
            map[row_list[0]] = int(row_list[len(row_list) - 1])

    with open(file_2, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row_list = list(row)
            if row_list[0] == "Username":
                continue
            map[row_list[0]] = map[row_list[0]] - int(row_list[len(row_list) - 1])

    print(map)

    with open('output/solve_diff.json', 'w+') as outfile:
        json.dump(map, outfile)


if __name__ == '__main__':
    file_1 = "output/rank_list_04-09-2020.csv"
    file_2 = "output/rank_list_28-08-2020.csv"
    solve(file_1, file_2)
