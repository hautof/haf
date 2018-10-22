import os, sys, json ,time, pytest
import allure
import warnings

from haf.SetUp import SetUp
from haf.run import Run
from haf.pylib.Log.LogController import LogController
from haf.pylib.Report.ReportWrite import ReportWrite
import haf.pylib.tools.globalvar as gl
from haf.pylib.Report.ReportPublic import ReportPublic
from haf.pylib.File.FileCopy import FileCopy
from haf.setup.TestCaseReplace import TestCaseReplace
from haf.pylib.tools.PlatformTool import PlatformTool
from haf.pylib.File.JsonTool import JsonTool


class FrameworkOfZhan(object):
    '''
    FrameworkOfZhan corpus-api 测试 主流程控制
    '''

    def __init__(self, **kwargs):
        self.class_name = "FrameworkOfZhan"
        self.logger = LogController.getLogger(self.class_name)
        if "logpath" in kwargs:
            self.logpath = kwargs["logpath"]
        else:
            self.logpath = "./data/log/"
        if "reportpath" in kwargs:
            self.reportpath = kwargs["reportpath"]
        else:
            self.reportpath = "./data/report/"
        
        gl._init()

    def runfromPy(self, filenames, allure=True, **kwargs):
        '''
        从 Python 文件执行

        :参数:

        * filename : Python 文件路径
        * allure : 默认为 True， 使用 allure 生成报告

        '''
        if isinstance(filenames, str):
            filenames = [filenames]
        if not isinstance(filenames, list):
            raise TypeError

        for f in filenames:
            if os.path.exists(f):
                pass
            else:
                self.logger.log_print("info", "can't find " + f, "runfromPy")
                filenames.remove(f)
        
        if "onefile" not in kwargs: # 默认方式，多个用例集
            filename_pys = ""
            filenum = 0
            for filename in filenames:
                filenum += 1
                self.logger.log_print("info", "start with " + filename, "runfromPy")
                
                allure_path = self.logpath
                filename_pure = filename.split("/")[-1].split(".")[-2]
                filename_pys = filename_pys + " " + filename

                report_path = self.reportpath + filename_pure
                allure_path = self.logpath + filename_pure

                if os.path.exists(report_path):
                    for i in range(1,20):
                        if os.path.exists(report_path + "_" + str(i)):
                            i +=1
                        else:
                            report_path = report_path + "_" + str(i)
                            break

                if os.path.exists(allure_path):
                    for i in range(1,20):
                        if os.path.exists(allure_path + "_" + str(i)):
                            i +=1
                        else:
                            allure_path = allure_path + "_" + str(i)
                            break
            self.pytestrun(filename_pys, filenum, allure_path)

            if allure:
                self.allurerun(allure_path, report_path, filename_pure)
            
            if "public2tomcat" in kwargs and kwargs["public2tomcat"] is True:
                #self.public2tomcat(report_path, kwargs["tomcatpath"])
                self.public2tomcat("data/report/" + filename_pure, kwargs["tomcatpath"])

    def runfromXlsx(self, filenames, allure=True, report_out_json=True, **kwargs):
        '''
        从 XLSX 文件执行

        :参数:

        * filename : xlsx 文件路径
        * allure : 默认为 True， 使用 allure 生成报告

        '''
        if isinstance(filenames, str):
            filenames = [filenames]
        if not isinstance(filenames, list):
            raise TypeError

        for f in filenames:
            if os.path.exists(f):
                pass
            else:
                self.logger.log_print("info", "can't find " + f, "runfromXlsx")
                filenames.remove(f)
        
        if "onefile" not in kwargs: # 默认方式，多个用例集
            filename_pys = ""
            filenum = 0
            for filename in filenames:
                filenum += 1
                self.logger.log_print("info", "start with " + filename, "runfromXlsx")
                setup = SetUp()
                allure_path = self.logpath
                setup.GenerateTestCasesFromXlsxFile(filename = filename, **kwargs)
                filename_py= filename.replace(".xlsx",".py")
                filename_pure = filename.split("/")[-1].split(".")[-2]
                filename_pys = filename_pys + " " + filename_py

                report_path = self.reportpath + filename_pure
                allure_path = self.logpath + filename_pure

                if os.path.exists(report_path):
                    for i in range(1,20):
                        if os.path.exists(report_path + "_" + str(i)):
                            i +=1
                        else:
                            report_path = report_path + "_" + str(i)
                            break

                if os.path.exists(allure_path):
                    for i in range(1,20):
                        if os.path.exists(allure_path + "_" + str(i)):
                            i +=1
                        else:
                            allure_path = allure_path + "_" + str(i)
                            break
            self.pytestrun(filename_pys, filenum, allure_path)
            if allure:
                self.allurerun(allure_path, report_path, filename_pure)
            
            if "public2tomcat" in kwargs and kwargs["public2tomcat"] is True:
                #self.public2tomcat(report_path, kwargs["tomcatpath"])
                self.public2tomcat("data/report/" + filename_pure, kwargs["tomcatpath"])
            if report_out_json:
                self.createrjsonofreport()

        else:
            onefilestr = "testcases/one.py"
            i = 0
            for filename in filenames: # 生成单个用例执行文件
                if i == 0:
                    gl.set_value("onefile_first", True)
                    i = 1
                self.logger.log_print("info", "start with " + filename, "runfromXlsx")
                setup = SetUp()
                filenum = 1
                allure_path = self.logpath
                setup.GenerateTestCasesFromXlsxFile(filename=filename, onefilestr=onefilestr, **kwargs)

            filename_py= onefilestr
            filename_pure = "one"

            report_path = self.reportpath + filename_pure
            allure_path = self.logpath + filename_pure

            if os.path.exists(report_path):
                for i in range(1,20):
                    if os.path.exists(report_path + "_" + str(i)):
                        i +=1
                    else:
                        report_path = report_path + "_" + str(i)
                        break

            if os.path.exists(allure_path):
                for i in range(1,20):
                    if os.path.exists(allure_path + "_" + str(i)):
                        i +=1
                    else:
                        allure_path = allure_path + "_" + str(i)
                        break
            
            self.pytestrun(filename_py, 1, allure_path)

            if allure:
                self.allurerun(allure_path, report_path, filename_pure)
            
            
            if "public2tomcat" in kwargs and kwargs["public2tomcat"] is True:
                #self.public2tomcat(report_path, kwargs["tomcatpath"])
                self.public2tomcat("data/report/" + filename_pure, kwargs["tomcatpath"])
            
            if report_out_json:
                self.createrjsonofreport()

    def pytestrun(self, filename, filenum, allure_path):
        '''
        执行 pytest 主程序，使用 --alluredir 生成 allure可以识别的 log

        :参数:

        * filename : pytest 可执行文件路径
        * filenum : pytest 可执行文件个数
        * allure_path : 生成的 allure 的 log 地址
        '''
        try:
            
            gl.set_value("start_time", self.logger.log_getsystime())
            runparam = "-s " + filename
            if filenum != 1:
                pass
                #runparam = runparam + " -n" + str(filenum)
            runparam += " --alluredir "  + allure_path 
            runparam += " --html "  + allure_path + "/mail.html"
            pytest.main(runparam)
            
            gl.set_value("finish_time", self.logger.log_getsystime())
            return True
        except Exception as e:
            self.logger.log_print("error", str(e), "pytestrun")
            return False

    def allurerun(self, logpath, reportpath, filename_pure, toOne=False):
        try:
            self.logger.log_print("debug", "start allurerun now...")
            if toOne is True:
                self.logger.log_print("debug", "allure to one file " + logpath)
                FileCopy.copy(logpath, "data/log/" + filename_pure)
                ReportWrite.createAllureReport("data/log/" + filename_pure, "data/report/" + filename_pure)
            else:
                self.logger.log_print("debug", logpath)
                ReportWrite.createAllureReport(logpath, "data/report/" + filename_pure)
            #ReportWrite.createAllureReport(logpath, reportpath)
        except Exception as e:
            self.logger.log_print("error", str(e), "allurerun")

    def public2tomcat(self, reportpath, tomcatpath):
        
        if PlatformTool.getPlatformIsLinux():
            casename = reportpath.split("/")[-1]
            ReportPublic.public2tomcat(reportpath, tomcatpath)
            self.logger.log_print("info", "report url : " + tomcatpath + casename + "/index.html")
        else:
            casename = reportpath.split("/")[-1]
            ReportPublic.public2tomcat(reportpath, tomcatpath)
          
		    
    def createrjsonofreport(self):
        testcases = gl.get_value("testcases")
        cjor = {}
        cjor["start_time"] = self.all2str(str(gl.get_value("start_time")))
        cjor["finish_time"] = self.all2str(str(gl.get_value("finish_time")))
        cjor["testsuites"] = []
        
        testsuites = {}
        for testcase in testcases:
            if testcase.name not in testsuites.keys():
                testsuites[testcase.name] = []
            testsuites[testcase.name].append(testcase)
        
        for key in testsuites.keys():            
            ct = {}
            ct["name"] = key
            ct["records"] = []
            for testcase in testsuites.get(key):
                ctr = {}
                ctr["name"] = self.all2str(testcase.api_name)
                ctr["path"] = self.all2str(testcase)
                if testcase.run:
                    ctr["status"] = "FAILED" if testcase.result is False or testcase.result is None else "PASSED"
                else:
                    ctr["status"] = "SKIPPED"
                ctr["start_time"] = self.all2str(testcase.start_time) 
                ctr["finish_time"] = self.all2str(testcase.finish_time)
                ctr["request"] = {
                    "method":self.all2str(testcase.api_method),
                    "url":self.all2str(testcase.api_protocol) + "://" +self.all2str(testcase.api_host_port) + self.all2str(testcase.api_url),
                    "path": "haf.testcase.HttpApiTestCase.HttpApiTestCase",
                    "headers":self.all2str(testcase.api_request_header),
                    "body":self.all2str(testcase.api_request_data),
                },
                ctr["response"] = {
                    "status_code":self.all2str(testcase.api_request_result),
                    "headers":self.all2str(str(testcase.api_response_header)),
                    "body":self.all2str(testcase.api_response)
                }
                ct["records"].append(ctr)
            cjor["testsuites"].append(ct)


        JsonTool.Write2File(json.dumps(cjor), "data/report/report.json")


    def all2str(self, input):
        if input is None:
            return "None"
        return str(input)


if __name__ == "__main__":
    foz = FrameworkOfZhan()
    foz.runfromXlsx("../data/Template.xlsx", public2tomcat=True, tomcatpath="/root/edison/tools/apache-tomcat-9.0.10/webapps/")
