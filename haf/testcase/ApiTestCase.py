#encoding='utf-8'

import os, time, sys

sys.path.append("..")

from haf.pylib.Log.LogController import LogController
from haf.testcase.TestCase_ import TestCase_

class ApiTestCase(TestCase_):
    '''
    ApiTest 实体
    '''
    def __init__(self):
        super(ApiTestCase, self).__init__()
        self.class_name = "ApiTestCase"
        self.logger = LogController.getLogger(self.class_name)
        self.initApiTestCase()
    
    def initApiTestCase(self):
        '''
        初始化 ApiTestCase
        '''
        self.AttrNoneList.append("api_request_data")
        self.AttrNoneList.append("api_request_result")
        self.AttrNoneList.append("initApiTestCase")
        
        self.api_name = ""
        self.api_url = ""
        self.api_protocol = ""

        self.api_request_data = None
        self.api_request_result = None

        self.api_response = None
        self.api_expect_response = None
