import json, os, sys

sys.path.append("..")

from haf.pylib.Log.LogController import LogController

class_name = "CheckHttpResponse"
logger = LogController.getLogger(class_name)


class CheckHttpResponse(object):
    '''
    检查 http response 是否相同
    '''
    def __init__(self):
        pass

    @staticmethod
    def CheckJson(result:dict, expect:dict, exclude:list):
        '''
        检查 json

        : result :  response 结果
        : expect :  期望的 response
        : exclude : 不比较的 key 列表
        '''
        if isinstance(result, dict) and isinstance(expect, dict) and isinstance(exclude, list):
            pass
        else:
            raise TypeError
        logger.log_print("debug", result, "CheckJson")
        logger.log_print("debug", expect, "CheckJson")
        for key in expect.keys():
            if not result.__contains__(key):
                return "result not has key : {}".format(key)
            if result[key] != expect[key] and key not in exclude:
                return "result not equal expect at : *{}* <result: {} > != <expect: {} >".format(key, str(result[key]),str(expect[key]))
        return True
        
    @staticmethod
    def CheckSql(result, expect, exclude):
        pass
