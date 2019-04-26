# encoding='utf-8'
'''
file name : apihelper
description : the api case helper
others:
    include request, response ...
'''
import json
from haf.common.database import SQLConfig
from haf.config import *


class Request(object):
    '''
    Request object of api request
    '''
    def __init__(self):
        self.header = {}
        self.data = {}
        self.url = ""
        self.method = ""
        self.protocol = ""
        self.host_port = ""
        self.url_part = ""

    def constructor(self, inputs: dict={}):
        '''
        constructor the Request by dict type
        :param inputs:
        :return:
        '''
        header = inputs.get("request_header")
        self.header = json.loads(header) if isinstance(header, str) else header
        data = inputs.get("request_data")
        try:
            self.data = json.loads(data) if isinstance(data, str) else data
        except Exception:
            self.data = data
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
        '''
        return the dict type
        :return:
        '''
        flag = False
        try:
            data = json.dumps(self.data, indent=4)
            data = str(self.data).encode('utf-8').decode('unicode')
            flag = True
        except:
            data = str(self.data)
        return {
            "header": str(self.header),
            "data": data if flag else str(self.data),
            "url": self.url,
            "method": METHOD_GROUP.get(str(self.method)),
            "protocol": self.protocol,
            "host_port": self.host_port
        }


class Response(object):
    '''
    Response
    '''
    def __init__(self):
        self.header = {}
        self.body = {}
        self.code = ""

    def constructor(self, inputs:dict={}):
        '''

        :param inputs:
        :return:
        '''
        self.header = inputs.get("header", {})
        self.body = inputs.get("body", {})
        self.code = inputs.get("code", {})

    def deserialize(self):
        '''

        :return:
        '''
        flag = False
        try:
            body = json.dumps(self.body, indent=4)
            body = str(self.body).encode('utf-8').decode('unicode')
            flag = True
        except:
            body = str(self.body)
        try:
            header = str(self.header).encode('utf-8').decode('unicode')
        except:
            header = str(self.header)
        return {
            "header": str(self.header),
            "body": body if flag else str(self.body),
            "code": self.code
        }


class Ids(object):
    '''
    api ids
    '''
    def __init__(self):
        self.id = ""
        self.subid = ""
        self.name = ""
        self.api_name = ""

    def constructor(self, inputs:dict={}):
        '''

        :param inputs:
        :return:
        '''
        self.id = inputs.get("id")
        self.subid = inputs.get("subid")
        self.name = inputs.get("name")
        self.api_name = inputs.get("api_name")

    def deserialize(self):
        '''

        :return:
        '''
        return {
            "id": self.id,
            "subid": self.subid,
            "name": self.name,
            "api_name": self.api_name
        }


class SqlInfo(object):
    '''
    sql info of api
    '''
    def __init__(self):
        self.scripts = {}
        self.config = None
        self.config_id = ""
        # for old cases
        self.check_list = {}

    def constructor(self, inputs:dict={}):
        '''

        :param inputs:
        :return:
        '''
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
        '''
        bind sql config
        :param config:
        :return:
        '''
        self.config = config

    def deserialize(self):
        '''
        :return:
        '''
        return {
            "scripts": self.scripts,
            "config": self.config.deserialize() if self.config is not None else None,
            "config_id": self.config_id,
            "check_list": self.check_list
        }


class Expect(object):
    '''
    expect of api
    '''
    def __init__(self):
        self.response = Response()
        self.sql_check_func = ""
        self.sql_response_result = {}

    def constructor(self, inputs:dict={}):
        '''

        :param inputs:
        :return:
        '''
        body = inputs.get("expect_response")
        self.response.body = json.loads(body) if isinstance(body, str) else body
        sql_check_func = inputs.get("expect_sql")
        if "None" in sql_check_func or sql_check_func is None:
            self.sql_check_func = None
        else:
            self.sql_check_func = sql_check_func.rsplit('.', 2)

    def deserialize(self):
        '''

        :return:
        '''
        return {
            "response": self.response.deserialize(),
            "sql_check_func": str(self.sql_check_func),
            "sql_response_result": self.sql_response_result
        }

