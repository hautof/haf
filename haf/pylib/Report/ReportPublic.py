#encoding='utf-8'
import os, sys, time

from haf.pylib.Log.LogController import LogController
from haf.pylib.tools.PlatformTool import PlatformTool
from haf.pylib.SQL.MysqlTool import MysqlTool
from haf.pylib.SQL.SQLConfig import SQLConfig

class_name = "ReportPublic"
logger = LogController.getLogger(class_name)


class ReportPublic(object):
    '''
    Public Report to Server
    '''
    def __init__(self):
        pass

    @staticmethod
    def public2sql(sqlconfig, teatcase):
        pass

    @staticmethod
    def public2tomcat(reportpath, tomcatpath):
        '''
        发布到 tomcat 服务下

        : reportpath : 生成的 报告 路径
        : tomcatpath : tomcat 的 webapps 地址
        '''
        logger.log_print("info", "start publish to " + tomcatpath, "public2tomcat") 
        if PlatformTool.getPlatformIsLinux():
            if os.path.exists(reportpath) and os.path.exists(tomcatpath):
                os.system("cp -rf " + reportpath + " " + tomcatpath )
        if PlatformTool.getPlatformIsWindows():
            if os.path.exists(reportpath) and os.path.exists(tomcatpath):

                reportpath = reportpath.replace("/", "\\") + "\\*"
                cmdstr = "xcopy /y /e /i /q " + reportpath + " " + tomcatpath
                logger.log_print("debug", cmdstr)
                os.system(cmdstr )
        
        logger.log_print("info", "success", "public2tomcat") 

        