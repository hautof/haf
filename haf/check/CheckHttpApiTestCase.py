#encoding='utf-8'

import os, sys

from haf.pylib.Log.LogController import LogController
from haf.testcase.HttpApiTestCase import HttpApiTestCase

class CheckHttpApiTestCase(object):
    '''
    检查原始数据是否可以生成用例 实体
    '''
    class_name = "CheckHttpApiTestCase"
    logger = LogController.getLogger(class_name)
    def __init__(self):
        self.class_name = "CheckHttpApiTestCase"
        self.logger = LogController.getLogger(self.class_name)

    @classmethod
    def checkKwargs(self, httpapitestcase, *args, **kwargs):
        '''
        检查 args 数据
        '''
        self.logger.log_print("info", "start", "checkWargs")
        if not isinstance(httpapitestcase, HttpApiTestCase):
            self.logger.log_print("error", "httpapitestcase is not %s, it's %s" % (HttpApiTestCase,type(httpapitestcase)), "checkKwargs")
            return False
        attrs = dir(httpapitestcase)
        if len(args) > 0:
            arg = args[0]
            for attr in attrs:
                if str(attr).startswith('__') and str(attr).endswith('__'):
                    continue
                if attr not in arg.keys():
                    if attr not in httpapitestcase.AttrNoneList:
                        self.logger.log_print("error", "check args attr : %s is not found in xlsx file" % attr, "checkKwargs")
                        return False
                    else:
                        self.logger.log_print("debug", "check args attr : %s is found in AttrNoneList" % attr, "checkKwargs")
                        continue
                else:
                    self.logger.log_print("debug", "check args attr : %s is found in xlsx file = %s" % (attr, arg.get(attr)), "checkKwargs")
                    continue
        else:   
            for kwarg in kwargs:         
                for attr in attrs:
                    if attr not in kwargs:
                        if attr not in httpapitestcase.AttrNoneList:
                            self.logger.log_print("error", "attr : %s is not exist" % attr, "checkKwargs")
                            return False
                        else:
                            kwargs[attr] = None
        self.logger.log_print("info", "ok", "checkWargs")
        return True
            
    
    
