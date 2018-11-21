# encoding='utf-8'
import importlib
import json

from haf.common.database import SQLConfig

from haf.config import CASE_HTTP_API_METHOD_GET, CASE_HTTP_API_METHOD_POST


class Request(object):
    def __init__(self):
        self.header = {}
        self.data = {}
        self.url = ""
        self.method = ""
        self.protocol = ""

    def constructor(self, inputs:dict={}):
        self.header = json.loads(inputs.get("request_header"))
        self.data = json.loads(inputs.get("request_data"))
        method = inputs.get("method", CASE_HTTP_API_METHOD_GET)
        if str(method) == "get":
            self.method = CASE_HTTP_API_METHOD_GET
        elif str(method) == "post":
            self.method = CASE_HTTP_API_METHOD_POST

        self.protocol = inputs.get("protocl", "http")
        self.host_port = inputs.get("host_port")

        self.rul_part = inputs.get("url", "")
        self.url = "{}://{}{}".format(self.protocol, self.host_port, self.rul_part)


class Response(object):
    def __init__(self):
        self.header = {}
        self.body = {}
        self.code = ""

    def constructor(self, inputs:dict={}):
        self.header = inputs.get("header", {})
        self.body = inputs.get("body", {})
        self.code = inputs.get("code", {})


class Ids(object):
    def __init__(self):
        self.id = ""
        self.subid = ""
        self.name = ""
        self.api_name = ""

    def constructor(self, inputs:dict={}):
        self.id = inputs.get("id")
        self.subid = inputs.get("subid")
        self.name = inputs.get("name")
        self.api_name = inputs.get("api_name")


class SqlInfo(object):
    def __init__(self):
        self.scripts = {}
        self.config = None
        self.config_id = ""

    def constructor(self, inputs:dict={}):
        self.scripts["sql_response"] = inputs.get("sql_response")
        self.config_id = str(inputs.get("sql_config")) if inputs.get("sql_config") is not None else ""

    def bind_config(self, config:SQLConfig):
        self.config = config

class Expect(object):
    def __init__(self):
        self.response = Response()
        self.sql_check_func = ""
        self.sql_body_check_key = []
        self.sql_response_result = {}

    def constructor(self, inputs:dict={}):
        self.response.body = json.loads(inputs.get("expect_response"))
        self.sql_body_check_key = inputs.get("sql_getlist", [])
        sql_check_func = inputs.get("expect_sql")
        if "None" in sql_check_func or sql_check_func is None:
            self.sql_check_func = None
        else:
            model_path, class_name, func_name = sql_check_func.rsplit('.', 2)
            class_content = importlib.import_module(model_path)
            self.sql_check_func = getattr(getattr(class_content, class_name), func_name)




