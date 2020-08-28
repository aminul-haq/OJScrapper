from flask import Flask, Response, Request
from flask_pymongo import pymongo, PyMongo
from scrappers.vjudge_profile_details_scrapper import *
import db as database
import json
from flask import jsonify

app = Flask(__name__)


# app.config['MONGO_DBNAME'] = 'test'
# app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority'
# mongo = PyMongo(app)


@app.route("/")
def home():
    return "Hello, World!"


# test to insert data to the data base
@app.route("/dbtest")
def test():
    # client = pymongo.MongoClient(
    #     "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority")
    # db = client.get_database("test")

    print(database.db.list_collection_names())

    return "Connected to the data base!"


@app.route("/dbinsert/<string:car_price>", methods=["GET"])
def insert(car_price):
    splitted = car_price.split("_")
    model = splitted[0]
    price = int(splitted[1])
    database.db.test.insert_one({"name": model, "price": price})
    return "inserted"


@app.route("/dbquery/price/<string:model>", methods=["GET"])
def get_price(model):
    res = database.db.test.find({"name": model})
    res_list = [x for x in res]
    return Response(json.dumps(res_list,default=str),mimetype="application/json")


@app.route("/vjudge/<string:username>", methods=["GET"])
def get_vjudge_profile(username):
    return solve_details(username)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
