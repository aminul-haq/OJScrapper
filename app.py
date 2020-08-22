from flask import Flask
from scrappers.vjudge_profile_details_scrapper import *

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/vjudge/<string:username>", methods=["GET"])
def get_vjudge_profile(username):
    return solve_details(username)


app.run(port=5000)
