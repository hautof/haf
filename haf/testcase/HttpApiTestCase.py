#encoding='utf-8'

import os, sys, time, json

sys.path.append("..")

from haf.pylib.Log.LogController import LogController
from haf.testcase.ApiTestCase import ApiTestCase
from haf.pylib.File.JsonTool import JsonTool

class HttpApiTestCase(ApiTestCase):
    '''
    HttpApiTestCase 类，即 http api 测试主体
    '''

    def __init__(self):
        super(HttpApiTestCase, self).__init__()
        self.class_name = "HttpApiTestCase"
        self.logger = LogController.getLogger(self.class_name)
        self.initHttpApiTestCase()
    
    def initHttpApiTestCase(self):
        '''
        初始化 HttpApiTestCase
        '''
        self.logger.log_print("info", "start", "_init")
        self.AttrNoneList.append("sql_setup")
        self.AttrNoneList.append("sql_teardown")
        self.AttrNoneList.append("sql_get")
        self.AttrNoneList.append("expect_sql")
        self.AttrNoneList.append("initHttpApiTestCase")
        self.AttrNoneList.append("constructor")
        self.AttrNoneList.append("sql_get_result")
        self.AttrNoneList.append("start_time")
        self.AttrNoneList.append("finish_time")
        self.AttrNoneList.append("api_response_header")
        self.AttrNoneList.append("sql_setup_result")
        self.AttrNoneList.append("sql_teardown_result")
        self.AttrNoneList.append("getName")
        self.api_request_header = None
        self.api_host_port = None
        self.api_method = None
        self.api_response_exclude = None
        self.api_response_header = None

        self.sql_setup = None
        self.sql_setup_result = None
        self.sql_teardown = None
        self.sql_teardown_result = None
        self.sql_get = None
        self.expect_sql = None
        self.sql_config = None
        self.sql_get_result = None 
        self.sql_getlist = None

        self.subname = None
        self.description = None
        self.story = None
        self.start_time = None
        self.finish_time = None

    def constructor(self, *args, **kwargs):
        '''
        构造器
        '''
        args_init = {}
        if len(args) > 0 and isinstance(args[0], dict):
            args_init = args[0]
        else:
            args_init = kwargs
        self.api_expect_response = args_init.get("api_expect_response")
        self.api_name = args_init.get("api_name")
        self.api_protocol = args_init.get("api_protocol")
        self.api_request_data = JsonTool.Str2Json(args_init.get("api_request_data"))
        self.api_request_result = kwargs.get("api_request_result")
        self.api_response = args_init.get("api_response")
        self.api_url = args_init.get("api_url")
        self.error = args_init.get("error")
        self.expect_sql = args_init.get("expect_sql")
        self.id = args_init.get("id")
        self.name = args_init.get("name")
        self.result = args_init.get("result")
        self.run = args_init.get("run")
        self.sql_get = JsonTool.Str2List(args_init.get("sql_get"), ";")
        self.sql_setup = JsonTool.Str2List(args_init.get("sql_setup"), ";")
        self.sql_teardown = JsonTool.Str2List(args_init.get("sql_teardown"), ";")
        self.subid = args_init.get("subid")
        self.subname = args_init.get("subname")
        self.description = args_init.get("description")
        self.story = args_init.get("story")
        self.sql_config = args_init.get("sql_config")
        self.api_response_exclude = JsonTool.Str2List(args_init.get("api_response_exclude"), ",")
        self.api_request_header = JsonTool.Str2Json(args_init.get("api_request_header"))
        self.api_host_port = args_init.get("api_host_port")
        self.api_method = args_init.get("api_method")
        lofsql = [[y.replace(" ", "").strip() for y in x.split("|")]  for x in JsonTool.Str2List(args_init.get("sql_getlist"), ";")]
        self.sql_getlist = lofsql if len(lofsql) != 1 else lofsql[0]


    def __str__(self):
        self.attrstr = {}
        for x in dir(self):
            if not ( x.startswith("__") or x.endswith("__") ):
                self.attrstr[x] = getattr(self, x)
        return str(self.attrstr)

    def getName(self):
        return "{}-{}.{}.{}".format( self.id, self.subid, self.name, self.subname)

        
if __name__ == "__main__":
    hatc = HttpApiTestCase(id=1,abc=2)
    print(str(HttpApiTestCase))
