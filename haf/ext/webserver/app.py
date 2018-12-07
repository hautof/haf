# encoding = 'utf-8'

from flask import Flask
from flask_restful import abort, Api
from haf.ext.jinjia2report.report import Jinja2Report
from haf.ext.webserver.resources import *
from haf.config import *

app = Flask("haf-app")
api = Api(app)


@app.route("/")
def index() -> str:
    return f"""
    <html>
    <pre>{BANNER_STRS}
    </pre>
    <html>"""


@app.route("/report")
def report() -> str:
    ResultResource().get()
    report_stream = Jinja2Report.report_online(globalenv.get_global("results"))
    return report_stream

@app.route("/status")
def status() -> str:
    return '{"status": "ok"}'

def abort_if_not_exist():
    abort(404, message="404")


def web_server():
    api.add_resource(LoaderResource, "/loader")
    api.add_resource(RunnerResource, "/runner")
    api.add_resource(ResultResource, "/result")
    api.add_resource(DocResource, "/doc")
    app.run(debug=False, port=WEB_SERVER_PORT)


