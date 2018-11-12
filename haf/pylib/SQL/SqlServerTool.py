import os, sys, time, json

sys.path.append("..")

from haf.pylib.Log.LogController import LogController

import pymssql

class_name = "SqlServerTool"
logger = LogController.getLogger(class_name)


class SqlServerTool(object):
    '''
    SqlServer 工具类
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "SqlServerTool"


    def ConnectAndExecute(self, sqlconfig, sqlscript, **kwargs):
        '''
        连接到数据库并执行脚本

        :参数:

        * testcase ： testcase 实例
        * caseparam : 执行的 case 中对应的 脚本名称
        '''

        sqlconfig = sqlconfig
        self.connect_msql = None
        logger.log_print("info", "start connect to {}".format(str(sqlconfig.host)), "ConnectAndExecute")
        try:
            logger.log_print("info", "start connect to {}".format(str(sqlconfig.database)), "ConnectAndExecute")
            self.connect_msql = pymssql.connect(sqlconfig.host, sqlconfig.username, sqlconfig.password, sqlconfig.database)

            cursor_m = self.connect_msql.cursor()
            data = []
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    if ss != None and ss != "None" and "None" not in ss:
                        logger.log_print("info", "start execute {}".format(ss), "ConnectAndExecute")
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        logger.log_print("info", "result {}".format(str(data)) ,"ConnectAndExecute")

            elif isinstance(sqlscript, str):
                if sqlscript != None or sqlscript != "None":
                    logger.log_print("info", "start execute {}".format(sqlscript), "ConnectAndExecute")
                    cursor_m.execute(sqlscript)
                    data = cursor_m.fetchall()
                    self.connect_msql.close()
                    
                    logger.log_print("info", "result {}".format(str(data)), "ConnectAndExecute")

                else :
                    self.connect_msql.close()
                    return False
            self.connect_msql.close()
            return data
        except Exception as e:
            logger.log_print("error", str(e), "ConnectAndExecute")
            if self.connect_msql is not None :
                self.connect_msql.close()

    def close(self):
        if self.connect_msql is not None:
            self.connect_msql.close()

if __name__ == "__main__":
    
    connect_msql = pymssql.connect("192.168.41.102", "uat", "111111", "ERP_DB")