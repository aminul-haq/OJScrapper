import os

from flask import Flask, send_from_directory, render_template

def page_not_found(e):
        return render_template('404.html'), 404

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.register_error_handler(404, page_not_found)
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/<path:path>')
    def send(path):
        return render_template(path + '.html')

    return app
