import json, os, sys

sys.path.append("..")

from haf.pylib.Log.LogController import LogController

class_name = "CheckHttpResponse"
logger = LogController.getLogger(class_name)


class CheckHttpResponse(object):
    def __init__(self):
        pass

    @staticmethod
    def CheckJson(result:dict, expect:dict, exclude:list):
        if isinstance(result, dict) and isinstance(expect, dict) and isinstance(exclude, list):
            pass
        else:
            raise TypeError
        logger.log_print("debug", result, "CheckJson")
        logger.log_print("debug", expect, "CheckJson")
        for key in expect.keys():
            if not result.__contains__(key):
                return "result not has key : " + key
            if result[key] != expect[key] and key not in exclude:
                return "result not equal expect at : " + key + " <result:" + str(result[key]) + "> != <expect:" + str(expect[key]) + ">"
        return True
            
