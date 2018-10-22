#encoding='utf-8'

import os, sys
from datetime import datetime

from haf.pylib.Log.LogController import LogController
from haf.testcase.HttpApiTestCase import HttpApiTestCase

class_name = "CheckSQLGet"
logger = LogController.getLogger(class_name)


class CheckSQLGet(object):
    '''
    检查 sql 结果与 response 是否相同
    '''
    def __init__(self):
        pass

    @staticmethod
    def Check(sqlr, resr):
        '''
        检查 SLQ 与 response

        '''
        #logger.log_print("debug", "start", "Check")
        logger.log_print("debug", type(sqlr), "Check")
        if sqlr is None or resr is None:
            return resr == sqlr
        elif isinstance(sqlr, datetime):
            try:
                resr = datetime.strptime(resr, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(e)
            return CheckSQLGet.CheckDateTime(sqlr, resr)
        else:
            return type(sqlr)(resr) == sqlr
        

    @staticmethod
    def CheckDateTime(datetime1, datetime2):
        '''
        检查 类型 为 datetime 的值
        '''
        #logger.log_print("debug", "start", "CheckDateTime")
        l = ['year', 'month', 'day', 'hour', 'minute','second']
        for x in l:
            if getattr(datetime1, x) == getattr(datetime2, x):
                continue
            else:
                return False

        #logger.log_print("debug", "ok", "CheckDateTime")
        return True