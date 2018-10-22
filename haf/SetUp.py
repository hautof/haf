import os, sys, time, json
import pytest

import haf.pylib.tools.globalvar as gl
from haf.pylib.Log.LogController import LogController
from haf.testcase.TestCaseController import TestCaseController, HttpApiTestCase
from haf.pylib.File.FileRead import FileRead
from haf.codegenerator.PytestCode import PytestCode
from haf.pylib.SQL.SQLConfig import SQLConfig
from haf.check.CheckHttpApiTestCase import CheckHttpApiTestCase
from haf.setup.TestCaseReplace import TestCaseReplace


class SetUp(object):
    '''
    框架初始化主程序， 主要用来生成 testcase 和 可执行代码
    '''
    def __init__(self):
        '''
        SetUp 初始化 logger 和 PytestCode
        '''
        self.class_name = "SetUp"
        self.logger = LogController.getLogger(self.class_name)
        self.pytestcode = PytestCode()

    def __str__(self):
        '''
        SetUp str 函数，返回 class_name
        '''
        return self.class_name

    def GenerateTestCasesFromXlsxFile(self, filename, sheetname="testcases", pytest=True, **kwargs):
        '''
        从 XLSX 文件 生成 TestCases(HttpApiTestCase)

        :参数: 
        * filename : str xlsx 文件路径
        * sheetname : str 默认 testcases, xlsx 文件的表名
        * pytest : bool 默认 True, 生成 pytest 可执行文件

        :return: TestCases
        '''
        self.logger.log_print("info", " start ", "GenerateTestCasesFromXlsxFile")
        self.logger.log_print("debug", filename, "GenerateTestCasesFromXlsxFile")


        fr = FileRead()
        xlsx = fr.open(filename)
        sheetofcases = xlsx.readSheetbyName(sheetname) # 读取 testcases 表
        sheetofconfigs = xlsx.readSheetbyName("config") # 读取 config 表
        
        rows = xlsx.getRows(sheetofcases)
        testcases = []
        getheader = True

        keys = {}
        key_index = 1
        for row in rows:
            for cell in row:
                keys[str(key_index)] = cell.value
                key_index += 1
            break

        for row in rows:
            self.logger.log_print("info", ".......................................................")
            rows_dict = {}
            i = 1
            for cell in row:
                if keys[str(i)] == "sql_config" :
                    if cell.value is None:
                        rows_dict[keys[str(i)]] = None
                    else:
                        rows_dict[keys[str(i)]] = self.ReadSqlConfigBySqlId(xlsx.getRows(sheetofconfigs), cell.value) # 从 config 表中查找 id 当前行的 数据库配置
                else:
                    rows_dict[keys[str(i)]] = cell.value
                i += 1
            
            for x in range(1,len(keys)):
                if rows_dict[keys[str(x)]] is None:
                    continue
                else:                    
                    testcasecontroller = TestCaseController()
                    
                    testcase = HttpApiTestCase()
                    if CheckHttpApiTestCase.checkKwargs(testcase, rows_dict):
                        testcase = testcasecontroller.CreateHttpApiTestCase(rows_dict)
                        if "ids" not in kwargs:
                            testcases.append(testcase)
                        else:
                            ids = [str(id) for id in kwargs["ids"]]
                            if str(testcase.id)+"."+str(testcase.subid) in kwargs["ids"]:
                                testcases.append(testcase)
                                self.logger.log_print("info", ".......................................................", str(testcase.id) + "." + str(testcase.subid))
                    break
                
        
        filename = filename.split(".")[-2]
        if "onefile" not in kwargs:
            self.pytestcode.generateCodeFile(testcases, filename=filename)
        else :
            self.pytestcode.generateCodeFile(testcases, filename=filename, **kwargs)
        
        self.logger.log_print("info", "---> debug 0")
        if gl.get_value("testcases") is None:
            self.logger.log_print("info", "---> debug 1" + str(testcases))
            gl.set_value("testcases", testcases)
        else:
            self.logger.log_print("info", "---> debug 2")
            cases = gl.get_value("testcases")
            for case in testcases:
                cases.append(case)
            gl.set_value("testcases", gl.get_value("testcases"))
        
        self.logger.log_print("info", "---> debug x" + str(testcases))
        xlsx.close()
        return testcases
        
    def ReadSqlConfigBySqlId(self, rows, sql_id):
        '''
        从 config 表中读取 id 为 sql_id 的数据库配置
        
        :参数: 
        * rows : rows 表行
        * sql_id : int 数据库 配置 id

        :return: sql_config
        '''

        self.logger.log_print("info", " start ", "ReadSqlConfigBySqlId")
        keys = {}
        key_index = 1
        find_by_id = False
        sqlconfig = SQLConfig()
        rows_dict = {}
        for row in rows:
            for cell in row:
                keys[str(key_index)] = cell.value
                key_index += 1
            break

        for row in rows:
            i = 1
            for cell in row:
                rows_dict[keys[str(i)]] = cell.value
                if keys[str(i)] == "id" and str(cell.value)==str(sql_id):
                    find_by_id = True
                i += 1
            if find_by_id:
                sqlconfig.constructor(rows_dict)
                break
        
        self.logger.log_print("info", str(rows_dict), "ReadSqlConfigBySqlId")
        self.logger.log_print("info", " ok ", "ReadSqlConfigBySqlId")
        return sqlconfig



if __name__ == "__main__":
    su = SetUp()
    testcases = su.GenerateTestCasesFromXlsxFile("../data/Template.xlsx")
    testcase = testcases[0]
    print (testcase.name)
    print (testcase.id)
    print (testcase.subid)
    