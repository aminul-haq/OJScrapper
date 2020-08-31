from flask import Flask, Response, Request, render_template, url_for, redirect
from flask_pymongo import pymongo, PyMongo
from scrappers.vjudge_profile_details_scrapper import *
import db as database
import json
from flask import jsonify
from forms import NewUsername

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc'


@app.route("/", methods=["GET", "POST"])
def home():
    form = NewUsername()
    if form.validate_on_submit():
        return redirect(url_for('get_vjudge_profile', username=form.username.data))
    return render_template('index.html', form=form)


@app.route("/vjudge/<string:username>", methods=["GET", "POST"])
def get_vjudge_profile(username):
    print(solve_details(username))
    return render_template('list.html', username=solve_details(username))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
