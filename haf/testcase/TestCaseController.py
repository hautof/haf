import os,sys

sys.path.append("..")

from haf.pylib.Log.LogController import LogController
from haf.testcase.HttpApiTestCase import HttpApiTestCase

class TestCaseController(object):
    '''
    管理生成 TestCase 的主体
    '''
    def __init__(self):
        self.class_name = "TestCaseController"
        self.logger = LogController.getLogger(self.class_name)

    def CreateHttpApiTestCase(self, *args, **kwargs):
        '''
        生成 HttpApiTestCase

        :参数:
        * args : 每个 xlsx 行 所对应的 dict
        * kwargs : 其他参数，暂不支持

        :return: HttpApiTestCase
        '''
        hatc = HttpApiTestCase()
        hatc.constructor(*args, **kwargs)
        return hatc


if __name__=="__main__":
    tcc = TestCaseController()
    print(tcc.CreateHttpApiTestCase())
        
