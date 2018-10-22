import os, sys, time, json
import pytest
import threading
import allure

from haf.pylib.Log.LogController import LogController
from haf.testcase.TestCaseController import TestCaseController
from haf.pylib.File.FileRead import FileRead
import haf.pylib.tools.globalvar as gl
from haf.pylib.Http.HttpController import HttpController
from haf.pylib.SQL.SQLTool import SQLTool
from haf.pylib.File.JsonTool import JsonTool
from haf.check.CheckHttpResponse import CheckHttpResponse
from haf.pylib.tools.debugprint import *
from haf.setup.TestCaseReplace import TestCaseReplace
#from haf.thirdparty.sqlcheck import sqlcheck
import urllib.request
import importlib


class_name = "Run"
logger = LogController.getLogger(class_name)
mst = SQLTool()

class Run(object):
    '''
    pytest 执行文件的主执行程序
    '''
    def __init__(self):
        pass

    @staticmethod
    def run(parameters):
        '''
        每个 testcase 都会执行的程序

        * parameters: str 执行 的用例的名称， 用来获取对应的存取的实例
        
        '''
        testcase = gl.get_value(parameters)
        
        logger.log_print("info", "start <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  " + parameters + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", "run")
        logger.log_print("info", parameters, "run")

        testcase.start_time = logger.log_getsystime()
        testcase.result = False

        testcase.finish_time = logger.log_getsystime()
        Run.SqlInit_step(testcase, casestr = str(testcase), sqlscript = getattr(testcase, "sql_setup"), sqlconfig = getattr(testcase, "sql_config").host)
    
        testcase.finish_time = logger.log_getsystime()
        result = Run.RunHttpRequest_step(testcase, casestr = str(testcase), url = getattr(testcase, "api_url"), data = getattr(testcase, "api_request_data"), protocol =  getattr(testcase, "api_protocol"))
        
        testcase.finish_time = logger.log_getsystime()
        Run.CheckHttpBody_step(testcase, result, casestr = str(testcase), response = getattr(testcase, "api_response"), expect = getattr(testcase, "api_expect_response"), exclude = getattr(testcase, "api_response_exclude"))
    
        testcase.finish_time = logger.log_getsystime()
        Run.SqlGet_step(testcase, sql_script=testcase.sql_get, sql_expect=getattr(testcase, "expect_sql"))

        testcase.finish_time = logger.log_getsystime()
        Run.SqlGetResultCheck_step(testcase, sql_get_result=testcase.sql_get_result, sql_expect=getattr(testcase, "expect_sql"))

        testcase.finish_time = logger.log_getsystime()
        Run.SqlTeardown_step(testcase, sqlscript = getattr(testcase, "sql_teardown"), sqlconfig = getattr(testcase, "sql_config").host)

        testcase.finish_time = logger.log_getsystime()
        logger.log_print("info", "ok <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< " + parameters + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", "run")

    @staticmethod
    @allure.step('Http Request')
    def RunHttpRequest_step(testcase, **kwargs):
        '''
        执行 http 请求

        :参数:

        * pv : testcase 实体

        :return: 返回请求的 结果
        '''
        protocol = getattr(testcase, "api_protocol")
        host_port = getattr(testcase, "api_host_port")
        url = protocol + "://" + host_port + getattr(testcase, "api_url")
        logger.log_print("info", url)
        data = getattr(testcase, "api_request_data")
        header = getattr(testcase, "api_request_header")

        tcr = TestCaseReplace()
        header = tcr.switch(header)
        setattr(testcase,"api_request_header", header)
        data = tcr.switch(data)
        setattr(testcase, "api_request_data", data)

        
        if getattr(testcase, "api_method").lower() == "get":
            result = HttpController.get(url, data, header)
        elif getattr(testcase, "api_method").lower() == "post":
            result = HttpController.post(url, data, header)
        elif getattr(testcase, "api_method").lower() == "put":
            result = HttpController.put(url, data)
        logger.log_print("info", result)
        if isinstance(result,urllib.request.URLError):
            testcase.api_response =  {}
            testcase.api_request_result = result.code
            testcase.api_response_header = result.info()
            testcase.result = False
        else:
            testcase.api_response =  JsonTool.Str2Json(result.read())
            testcase.api_request_result = result.code
            testcase.api_response_header = result.info()
        return testcase.api_response

    @staticmethod
    def CaseReplace(testcase):
        tcr = TestCaseReplace()
        for attr in dir(testcase):
            if isinstance(getattr(testcase, attr), dict) and not attr.startswith("__") and not attr.endswith("__") and "othercasezhan" in getattr(testcase, attr):
                tcr.switch(getattr(testcase, attr))

    @staticmethod
    @allure.step('Check Http Response Body ')
    def CheckHttpBody_step(testcase, result, **kwargs):
        '''
        执行 http 请求结果检查

        :参数: 

        * testcase : testcase 实体
        * result ： http 请求 结果

        :return: check_result
        '''
        logger.log_print("info", "start", "CheckHttp")        
        result = result
        expect = JsonTool.Str2Json(getattr(testcase, "api_expect_response"))
        exclude = JsonTool.Str2List(getattr(testcase, "api_response_exclude"), ",")
        logger.log_print("info", str(result), "CheckHttp")
        check_result = CheckHttpResponse.CheckJson(result, expect, exclude)
        if len(expect.keys()) != 0:
            testcase.result = result
        assert check_result==True

        '''if check_result is True:  
            logger.log_print("info", "OK", "CheckHttp")
            return True
        else:
            logger.log_print("info", "Failed", "CheckHttp")
            return check_result
           ''' 
        
    @staticmethod
    def getIdSubidName(pv):
        return getattr(pv, "id")


    @staticmethod
    @allure.step("SQL Init")
    def SqlInit_step(testcase, **kwargs):
        '''
        执行 sql init

        :参数:

        * testcase ： testcase 实体
        '''
        tcr = TestCaseReplace()
        testcase.sql_teardown = tcr.switch(testcase.sql_setup)
        logger.log_print("debug", str(testcase.sql_setup), "SQL Init")
        testcase.sql_setup_result = mst.ConnectAndExecute(testcase.sql_config, testcase.sql_setup)
        logger.log_print("debug", str(testcase.sql_setup_result), "SQL Init")
    
    @staticmethod
    @allure.step("SQL Teardown")
    def SqlTeardown_step(testcase, **kwargs):
        '''
        执行 sql teardown

        :参数:

        * testcase ： testcase 实体
        '''
        tcr = TestCaseReplace()
        testcase.sql_teardown = tcr.switch(testcase.sql_setup)
        logger.log_print("debug", str(testcase.sql_teardown), "SQL Teardown")
        testcase.sql_teardown_result = mst.ConnectAndExecute(testcase.sql_config, testcase.sql_teardown)
        logger.log_print("debug", str(testcase.sql_teardown_result), "SQL Teardown")

    @staticmethod
    @allure.step("SQL Get By Script")
    def SqlGet_step(testcase, **kwargs):
        '''
        执行 sql get
        
        :参数:

        * testcase ： testcase 实体
        '''
        tcr = TestCaseReplace()
        testcase.sql_get = tcr.switch(testcase.sql_get)
        logger.log_print("debug", str(testcase.sql_get), "SqlGet")
        testcase.sql_get_result = mst.ConnectAndExecute(testcase.sql_config, testcase.sql_get)
        logger.log_print("debug", str(testcase.sql_get_result), "SqlGet")
    
    
    @staticmethod
    @allure.step("SQL Get Result Check")
    def SqlGetResultCheck_step(testcase, **kwargs):
        '''
        执行 sql get
        
        :参数:

        * testcase ： testcase 实体
        '''

        logger.log_print("debug", str(testcase.sql_get_result), "SqlGetResultCheck_step")
        fullname = testcase.expect_sql
        if "None" in fullname:
            return True
        model_path, class_name, func_name = fullname.rsplit('.',2)
        logger.log_print("debug", model_path + " " + func_name)

        class_content = importlib.import_module(model_path)
        func = getattr(getattr(class_content, class_name), func_name)

        result = func(testcase.sql_get_result, testcase.api_response, testcase.sql_getlist, testcase=testcase)
        testcase.result = result
        assert result==True
        #testcase.sql_get_result = mst.ConnectAndExecute(getattr(testcase,"sql_config"), getattr(testcase, "sql_get"))
