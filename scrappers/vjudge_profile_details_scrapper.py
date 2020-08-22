import requests
from bs4 import BeautifulSoup
import json
import pandas

def solve_details(handle):
    url = "https://vjudge.net/user/solveDetail/" + handle
    response = requests.get(url)
    # soup = BeautifulSoup(response.text, "html.parser")
    solve_data = json.loads(response.text)
    #print(solve_data)
    #return solve_data
    #print(pandas.json_normalize(solve_data).to_html)
    return pandas.json_normalize(solve_data).to_html()


def get_handles_list():
    handles = ["sarwar_khalid", "Pharaoh28", "arfaqur", "abdullah_mahmud7", "FairoozR", "necromancer", "bashem",
               "Wasi00007", "trk111", "NadmanKhan", "Moumi_", "toufique525", "2011046642_Opy", "vedistaan",
               "TaneemAhmed", "maxim_v2", "Fahimmanowar", "Junayed_Hasan", "maruf22", "Jushraf", "RifatXia",
               "Rejuana", "omi_farhan75", "OmarHaroon", "Tajreean_Ahmed", "Tayeb183", "Simanta_Mostafa", "MaishaAmin",
               "arman39", "Lamia_Munira", "Ahamed_TJ", "ripcode", "Sunjaree", "ms166", "Antony_Wu"]
    return handles


if __name__ == '__main__':
    solve_details("aminul1")
