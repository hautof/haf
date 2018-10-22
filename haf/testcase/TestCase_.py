#encoding='utf-8'

import os, time, sys

sys.path.append("..")

from haf.pylib.Log.LogController import LogController

class TestCase_(object):
    '''
    TestCase 基类， 包含测试用例所需要最少的 特征
    '''
    def __init__(self):
        self.class_name = "TestCase_"
        self.logger = LogController.getLogger(self.class_name)
        self.initTestCase()
    
    def initTestCase(self):
        '''
        初始化 测试用例基本内容
        '''
        self.logger.log_print("info", "_init start", "_init")
        self.AttrNoneList = ["result", "error", "AttrNoneList", "class_name", "initTestCase", "logger"]
        self.id = ""
        self.name = ""
        self.subid = ""
        self.run = True
        # testcase results
        self.result = False
        self.error = ""


    