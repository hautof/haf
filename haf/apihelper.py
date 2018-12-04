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
        self.host_port = ""
        self.url_part = ""

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

        self.url_part = inputs.get("url", "")
        self.url = f"{self.protocol}://{self.host_port}{self.url_part}"

    def deserialize(self):
        try:
            data = json.dumps(self.data, indent=4)
        except:
            data = str(self.data)
        return {
            "header": self.header,
            "data": data,
            "url": self.url,
            "method": self.method,
            "protocol": self.protocol,
            "host_port": self.host_port
        }


class Response(object):
    def __init__(self):
        self.header = {}
        self.body = {}
        self.code = ""

    def constructor(self, inputs:dict={}):
        self.header = inputs.get("header", {})
        self.body = inputs.get("body", {})
        self.code = inputs.get("code", {})

    def deserialize(self):
        try:
            body = json.dumps(self.body, indent=4)
        except:
            body = str(self.body)
        return {
            "header": str(self.header),
            "body": body,
            "code": self.code
        }


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

    def deserialize(self):
        return {
            "id": self.id,
            "subid": self.subid,
            "name": self.name,
            "api_name": self.api_name
        }


class SqlInfo(object):
    def __init__(self):
        self.scripts = {}
        self.config = None
        self.config_id = ""
        # for old cases
        self.check_list = {}

    def constructor(self, inputs:dict={}):
        sql_response = inputs.get("sql_response")
        if ";" in sql_response:
            self.scripts["sql_response"] = sql_response.split(";")
        else:
            self.scripts["sql_response"] = [sql_response]

        sql_check_list = inputs.get("sql_response_check_list")
        self.check_list["sql_response"] = []
        if ";" in sql_check_list:
            for x in sql_check_list.split(";"):
                self.check_list["sql_response"].append([y.replace(" ", "").strip() for y in x.split("|")])
        else:
            self.check_list["sql_response"].append([y.replace(" ", "").strip() for y in sql_check_list.split("|")])

        self.config_id = str(inputs.get("sql_config")) if inputs.get("sql_config") is not None else ""

    def bind_config(self, config:SQLConfig):
        self.config = config

    def deserialize(self):
        return {
            "scripts": self.scripts,
            "config": self.config.deserialize() if self.config is not None else None,
            "config_id": self.config_id,
            "check_list": self.check_list
        }


class Expect(object):
    def __init__(self):
        self.response = Response()
        self.sql_check_func = ""
        self.sql_response_result = {}

    def constructor(self, inputs:dict={}):
        self.response.body = json.loads(inputs.get("expect_response"))
        sql_check_func = inputs.get("expect_sql")
        if "None" in sql_check_func or sql_check_func is None:
            self.sql_check_func = None
        else:
            self.sql_check_func = sql_check_func.rsplit('.', 2)

    def deserialize(self):
        return {
            "response": self.response.deserialize(),
            "sql_check_func": str(self.sql_check_func),
            "sql_response_result": self.sql_response_result
        }

