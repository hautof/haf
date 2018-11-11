#encoding="utf-8"

import os, sys, time, json
import pytest


from haf.pylib.Log.LogController import LogController
from haf.testcase.HttpApiTestCase import HttpApiTestCase
import haf.pylib.tools.globalvar as gl
from haf.pylib.tools.languageTool import languageTool

class PytestCode(object):
    '''
    生成 pytest 可执行文件
    '''
    def __init__(self):
        self.class_name = "PytestCode"
        self.logger = LogController.getLogger(self.class_name)

    def generateCodeFile(self, testcases:dict, codefilepath=None, **kwargs):
        '''
        生成 python 文件

        :参数:
        * testcases ： 所有的用例
        * codefilepath : 默认与 用例所在位置相同
        
        '''
        self.logger.log_print("info", "start")
        if len(testcases) > 0:
            if not isinstance(testcases[0], HttpApiTestCase):
                return False
        else:
            return False
        self.case_name = ""
        if "filename" in kwargs:
            filename = kwargs["filename"] + ".py"
            self.case_name = languageTool.Chinese2English(kwargs["filename"].split("/")[-1])
            self.logger.log_print("debug", self.case_name)
        else:
            filename = "default.py"

        if codefilepath is None:
            codefilepath = filename
        else : 
            codefilepath = codefilepath + "/" + filename
        
        if "onefilestr" in kwargs: # 复写 codefilepath
            codefilepath = kwargs["onefilestr"] 

        
        if gl.get_value("onefile_first") is True:
            gl.set_value("onefile_first", False)
            cf = open(codefilepath, 'w')
            write_lines = """
import pytest, os, sys, allure
sys.path.append("../haf")
from haf.run import Run
#from haf.thirdparty.corpus_api.sqlcheck import sqlcheck
class Test_case_name:
        """
            write_lines = write_lines.replace("case_name", self.case_name)

        elif gl.get_value("onefile_first") is False:
            cf = open(codefilepath, 'a')
            write_lines = """

class Test_case_name:
        """
            write_lines = write_lines.replace("case_name", self.case_name)
        elif gl.get_value("onefile_first") is None:
            cf = open(codefilepath, 'w')
            write_lines = """
import pytest, os, sys, allure
sys.path.append("../haf")
from haf.run import Run
#from haf.thirdparty.corpus_api.sqlcheck import sqlcheck
class Test_case_name:
        """
            write_lines = write_lines.replace("case_name", self.case_name)

        for testcase in testcases:
            gcb = self.generateCodeBlock(testcase)
            if gcb == False:
                continue
            write_lines += gcb

        cf.writelines(write_lines)
        cf.close()

        self.logger.log_print("info", "ok")

    def generateCodeBlock(self, testcase:HttpApiTestCase):   
        '''
        根据每个 用例 生成 pytest 可识别的 方法
        '''
        if testcase.run is False:
            
            pycode_template = """
    @pytest.mark.skip(reason='Not Run')
    @allure.description("allure_description")
    @allure.story("allure_story")
    def test_pycode_template(self):
        Run.run("testcase_parameters")
        """
        else:
            pycode_template = """
    @allure.description("allure_description")
    @allure.story("allure_story")
    def test_pycode_template(self):
        Run.run("testcase_parameters")
        """
        if testcase.id is None and testcase.subid is None:
            return False
        temp = [str(self.case_name), str(testcase.name), str(testcase.id), str(testcase.subid), str(testcase.subname)]
        functionname = "{}_{}_{}_{}_{}".format(*temp)
        pycode_template = str(pycode_template)
        print (functionname)
        pycode_template = pycode_template.replace("pycode_template",str(functionname))
        params = functionname
        pycode_template = pycode_template.replace("testcase_parameters", params)
        pycode_template = pycode_template.replace("allure_description", str(testcase.description))
        pycode_template = pycode_template.replace("allure_story", str(testcase.story))
        gl.set_value(params, testcase)

        return pycode_template

