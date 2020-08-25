from flask import Flask
from flask_pymongo import pymongo
from scrappers.vjudge_profile_details_scrapper import *

# import db

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


# test to insert data to the data base
@app.route("/dbtest")
def test():
    client = pymongo.MongoClient(
        "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database("test")

    return "Connected to the data base!"


@app.route("/vjudge/<string:username>", methods=["GET"])
def get_vjudge_profile(username):
    return solve_details(username)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
