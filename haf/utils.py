# encoding = 'utf-8'
import os
import urllib

from haf.apihelper import Request, Response
from haf.common.database import MysqlTool
from haf.common.log import Log
from openpyxl import load_workbook

from haf.config import CASE_HTTP_API_METHOD_GET, CASE_HTTP_API_METHOD_POST, CASE_HTTP_API_METHOD_PUT
from haf.common.httprequest import HttpController

from http.client import HTTPResponse

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
            logger.log_print("debug", e)
        finally:
            logger.log_print("debug", func_obj)
            if func_obj is not None:
                func_obj.close()


    @staticmethod
    def get_rows_from_xlsx(filename):
        if not filename.endswith("xlsx"):
            return {}
        if not os.path.exists(filename):
            logger.error("not fount file : {}".format(filename))
            raise FileNotFoundError
        try:
            header = []
            config_header = []
            data = []
            config_data = []

            result = {}
            result["testcases"] = []
            result["configs"] = []

            xlsx = load_workbook(filename)
            sheet_names = xlsx.sheetnames
            if "testcases" not in sheet_names or "config" not in sheet_names:
                logger.log("not fount sheet in {}".format(filename))
                return {}
            testcases = xlsx["testcases"].rows
            config = xlsx["config"].rows
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

            for d in data:
                result["testcases"].append(dict(zip(header, d)))

            for d in config_data:
                result["configs"].append(dict(zip(config_header, d)))

            return result
        except Exception as e:
            logger.error(e)


    @staticmethod
    def http_request(request:Request) :
        header = request.header
        data = request.data
        method = request.method
        url = request.url

        response = Response()
        result = None
        if method == CASE_HTTP_API_METHOD_GET:
            result = HttpController.get(url, data, header)
        elif method == CASE_HTTP_API_METHOD_POST:
            result = HttpController.post(url, data, header)
        if method == CASE_HTTP_API_METHOD_PUT:
            result = HttpController.put(url, data, header)

        if isinstance(result, HTTPResponse):
            response.header = result.headers
            response.body = result.read()
            response.code = result.code
        elif isinstance(result,urllib.request.URLError) or isinstance(result, urllib.request.HTTPError) or isinstance(result, urllib.request.HTTPHandler):
            response.body =  {}
            response.code = result.code
            response.header = result.info()

        return response



