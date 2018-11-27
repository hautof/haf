# encoding = 'utf-8'

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from multiprocessing import Process
from haf.ext.webserver.resources import *
from haf.config import *

app = Flask("haf-app")
api = Api(app)


@app.route("/")
def index():
    return "welcome to use haf !"


def abort_if_not_exist():
    abort(404, message="404")


def web_server():
    api.add_resource(LoaderResource, "/loader")
    api.add_resource(RunnerResource, "/runner")
    api.add_resource(ResultResource, "/result")

    app.run(debug=False, port=WEB_SERVER_PORT)


