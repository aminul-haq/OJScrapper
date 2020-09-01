from flask import Flask, Response, Request
from flask_pymongo import pymongo, PyMongo
from scrappers.vjudge_profile_details_scrapper import *
import db as database
import json
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/vjudge/<string:username>", methods=["GET"])
def get_vjudge_profile(username):
    try:
        return solve_details(username), 200
    except:
        return "error", 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
