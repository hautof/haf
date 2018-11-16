# encoding='utf-8'

from haf.config import CASE_HTTP_API_METHOD_GET, CASE_HTTP_API_METHOD_POST


class Request(object):
    def __init__(self):
        self.header = {}
        self.data = {}
        self.url = ""
        self.method = ""
        self.protocol = ""

    def constructor(self, inputs:dict={}):
        self.header = inputs.get("header", {})
        self.data = inputs.get("data", {})
        self.url = inputs.get("url", "")
        method = inputs.get("method", CASE_HTTP_API_METHOD_GET)
        if str(method) == "get":
            self.method = CASE_HTTP_API_METHOD_GET
        elif str(method) == "post":
            self.method = CASE_HTTP_API_METHOD_POST

        self.protocol = inputs.get("protocl", "http")


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


class Expect(object):
    def __init__(self):
        self.response = Response()
        self.sql_check_func = ""
        self.sql_body_check_key = []

    def constructor(self, inputs:dict={}):
        self.response.constructor(inputs)
        self.sql_check_func = inputs.get("expect_sql")
        self.sql_body_check_key = inputs.get("sql_getlist", [])



