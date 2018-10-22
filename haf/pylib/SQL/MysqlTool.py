import os, sys, time, json

sys.path.append("../../../")
from haf.pylib.Log.LogController import LogController

import pymysql


class_name = "MysqlTool"
logger = LogController.getLogger(class_name)


class MysqlTool(object):
    '''
    Mysql 工具类
    '''
    def __init__(self):
        pass

    @staticmethod
    def ConnectAndExecute(sqlconfig, sqlscript, **kwargs):
        '''
        连接到数据库并执行脚本

        :参数:
        
        * sqlconfig ： sqlconfig 实例
        * sqlscript : 执行的 sqlscript 
        '''
        
        sqlconfig = sqlconfig
        connect_msql = None
        logger.log_print("info", "start connect to {}".format(str(sqlconfig.host)), "ConnectAndExecute")
        try:
            connect_msql = pymysql.connect(sqlconfig.host, sqlconfig.username, sqlconfig.password, sqlconfig.database)
            cursor_m = connect_msql.cursor()
            data = []
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    if ss != None and ss != "None" and "None" not in ss and len(ss)>5:
                        logger.log_print("info", "start execute {}".format(ss), "ConnectAndExecute")
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        logger.log_print("info", "result {}".format(str(data)) ,"ConnectAndExecute")
            return data
        except Exception as e:
            logger.log_print("error", str(e), "ConnectAndExecute")
            if connect_msql is not None :
                connect_msql.close()

if __name__ == "__main__":
    connect_msql = pymysql.connect("192.168.41.68", "xztest", "nC0Dq1xDH6uq[K1of0V1", "corpus_qa")
    cursor_m = connect_msql.cursor()
    cursor_m.execute("select * from tbl_toefl_paper")
    print(cursor_m.fetchall())