from flask import Flask, Response, url_for, render_template, send_from_directory
from flask_pymongo import pymongo, PyMongo
from scrappers.vjudge_profile_details_scrapper import *
import db as database
import json
import jinja2.exceptions
from flask import jsonify

app = Flask(__name__, instance_relative_config=True)


# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# app.register_error_handler(404, page_not_found)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def send(path):
    return render_template(str(path).replace(".html", "") + '.html')


# app.config['MONGO_DBNAME'] = 'test'
# app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority'
# mongo = PyMongo(app)

#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/<pagename>')
# def admin(pagename):
#     return render_template(pagename+'.html')
#
# @app.route('/<path:resource>')
# def serveStaticResource(resource):
# 	return send_from_directory('static/', resource)
#
#
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


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
    return Response(json.dumps(res_list, default=str), mimetype="application/json")


@app.route("/vjudge/<string:username>", methods=["GET"])
def get_vjudge_profile(username):
    return solve_details(username)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
