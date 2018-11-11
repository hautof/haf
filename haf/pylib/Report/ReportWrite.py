#__*__ encoding='utf-8'

import os, sys, time

from haf.pylib.Log.LogController import LogController
from haf.pylib.tools.PlatformTool import PlatformTool
import allure_pytest
class_name = "ReportWrite"
logger = LogController.getLogger(class_name)

class ReportWrite(object):
    '''
    报告生成工具

    目前有 : allure 
    '''
    def __init__(self):
        pass
    
    @staticmethod
    def createAllureReport(logpath:str, reportpath:str):
        '''
        生成 Allure 报告

        :参数: 
        * logpath ： 需要的 allure log 地址
        * reportpath ： 生成的 report 地址

        :return: bool
        '''
        localpath = os.path.split(os.path.realpath(__file__))[0]
        if PlatformTool.getPlatformIsWindows():
            allure_bin = os.path.abspath(os.path.join(localpath,"../../bin/allure/bin/allure.bat"))
        else:
            allure_bin = os.path.abspath(os.path.join(localpath,"../../bin/allure/bin/allure"))
            os.system("chmod +x " + allure_bin)
        
        cmdstr = allure_bin + " generate -c " + str(logpath) + " -o " + str(reportpath)
        print(cmdstr)
        os.system(cmdstr)
        return True