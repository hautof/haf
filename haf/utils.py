# encoding = 'utf-8'
import json
import os
import time
import traceback
import urllib

from haf.apihelper import Request, Response
from haf.common.database import MysqlTool
from haf.common.log import Log
from openpyxl import load_workbook
from haf.config import *
from haf.common.httprequest import HttpController
from http.client import HTTPResponse
import random
import platform
import yaml

logger = Log.getLogger(__name__)


class Utils(object):

    @staticmethod
    def sql_execute(sqlconfig, sqlscript, **kwargs):
        '''
        连接到数据库并执行脚本
        :参数:

        * testcase ： testcase 实例
        * caseparam : 执行的 case 中对应的 脚本名称
        '''
        key = kwargs.get("key")
        func_obj = None
        data = None
        try:
            sqlconfig = sqlconfig
            if sqlconfig.protocol == "mysql":
                 func_obj = MysqlTool()
            # elif sqlconfig.protocol == "sqlserver":
            #     func_obj = SqlServerTool()
            # elif sqlconfig.protocol == "redis":
            #     func_obj = RedisTool()
            # elif sqlconfig.protocol == "neo4j":
            #     func_obj = Neo4j()

            data = func_obj.connect_execute(sqlconfig, sqlscript, **kwargs)
            return data
        except Exception as e:
            logger.info("{} {}".format(key, e))
        finally:
            logger.info("{} {}".format(key, func_obj))
            if func_obj is not None:
                func_obj.close()

    @staticmethod
    def get_rows_from_xlsx(filename):
        '''
        :param filename: 文件名
        :return:
        '''
        if not filename.endswith("xlsx"):
            return {}
        if not os.path.exists(filename):
            logger.error("{} not fount file : {}".format("system$%util$%", filename))
            raise FileNotFoundError
        try:
            header = []
            config_header = []
            dbconfig_header = []
            data = []
            config_data = []
            dbconfig_data = []

            result = {}
            result["testcases"] = []
            result["dbconfig"] = []
            result["config"] = []

            xlsx = load_workbook(filename)
            sheet_names = xlsx.sheetnames
            if "testcases" not in sheet_names or "config" not in sheet_names:
                logger.log(f"not fount sheet in {filename}")
                return {}
            testcases = xlsx["testcases"].rows
            config = xlsx["config"].rows
            dbconfig = xlsx["dbconfig"].rows

            for row in testcases:
                header = [cell.value for cell in row if cell.value is not None]
                break

            for row in testcases:
                data.append([cell.value for cell in row])

            for row in config:
                config_header = [cell.value for cell in row if cell.value is not None]
                break

            for row in config:
                config_data.append([cell.value for cell in row])

            for row in dbconfig:
                dbconfig_header = [cell.value for cell in row if cell.value is not None]
                break

            for row in dbconfig:
                dbconfig_data.append([cell.value for cell in row])

            for d in data:
                result["testcases"].append(dict(zip(header, d)))

            for d in config_data:
                result["config"].append(dict(zip(config_header, d)))

            for d in dbconfig_data:
                result["dbconfig"].append(dict(zip(dbconfig_header, d)))
            return result
        except Exception as e:
            logger.error(e)

    @staticmethod
    def load_from_json(file_name):
        try:
            if os.path.exists(file_name):
                f = open(file_name, 'r', encoding='utf-8')
                result = json.loads(f.read())
                f.close()
                return result
            else:
                raise FileNotFoundError
        except Exception as e:
            traceback.print_exc()
            logger.error(e)

    @staticmethod
    def load_from_yml(file_name):
        try:
            if os.path.exists(file_name):
                f = open(file_name, 'r', encoding='utf-8')
                result = yaml.load(f)
                f.close()
                return result
            else:
                raise FileNotFoundError
        except Exception as e:
            traceback.print_exc()
            logger.error(e)

    @staticmethod
    def http_request(request:Request, **kwargs) :
        '''
        http request
        :param request: Request
        :return: Response
        '''
        key = kwargs.get("key")

        header = request.header
        data = request.data
        method = request.method
        url = request.url

        response = Response()
        result = None
        if method == CASE_HTTP_API_METHOD_GET:
            result = HttpController.get(url, data, header, **kwargs)
        elif method == CASE_HTTP_API_METHOD_POST:
            result = HttpController.post(url, data, header)
        if method == CASE_HTTP_API_METHOD_PUT:
            result = HttpController.put(url, data, header)

        logger.info("{} {}".format(key, result))
        if isinstance(result, HTTPResponse):
            response.header = result.headers
            try:
                response.body = json.loads(result.read())
            except :
                response.body = result.read()
            response.code = result.code
        elif isinstance(result,urllib.request.URLError) or isinstance(result, urllib.request.HTTPError) or isinstance(result, urllib.request.HTTPHandler):
            response.body =  {}
            response.code = result.code if hasattr(result, "code") else None
            response.header = result.info() if hasattr(result, "info") else None

        logger.info(f"{key} {result}")
        return response

    @staticmethod
    def get_datetime_now():
        '''
        get datetime now to str
        :return: time now str
        '''
        current_time = time.time()
        local_time = time.localtime(current_time)
        time_temp = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        secs = (current_time - int(current_time)) * 1000
        timenow = "%s %03d" % (time_temp, secs)
        return timenow

    @staticmethod
    def get_case_name():
        '''
        get datetime now to str
        :return: time now str
        '''
        current_time = time.time()
        local_time = time.localtime(current_time)
        time_temp = time.strftime("%Y-%m-%d-%H.%M", local_time)
        return time_temp

    @staticmethod
    def jsontool(input):
        '''
        deal with json object
        :param input:
        :return:
        '''
        try:
            output = json.loads(input)
            return output
        except Exception as e:
            traceback.print_exc()
            return {"input":input}

    @staticmethod
    def get_random_name():
        '''
        :return:
        '''
        return str(random.randint(100000, 999999))

    @staticmethod
    def get_platform():
        return platform.system()