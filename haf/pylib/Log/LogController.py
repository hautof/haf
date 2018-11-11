import os, sys, time

from haf.pylib.Log.LogShow import LogShow

class LogController(object):
    '''
    Log 管理
    '''

    def __init__(self):
        self.class_name = "LogController"

    def __str__(self):
        return self.class_name

    @classmethod
    def getLogger(self, logclass:str):
        '''
        生成 logger

        :参数:
        * logclass : 生成的 logger 标签

        :return: logger
        '''
        return LogShow(logclass)


if __name__ == "__main__":
    ls = LogController.getLogger("test")
    ls.log_print("warn", "teststestest")
    os.system("pause")
