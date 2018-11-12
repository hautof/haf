#encoding='utf-8'


from haf.pylib.Log.LogController import LogController

from haf.pylib.SQL.MysqlTool import MysqlTool

from haf.pylib.SQL.SqlServerTool import SqlServerTool

from haf.pylib.SQL.RedisTool import RedisTool

from haf.pylib.SQL.Neo4jTool import Neo4j

from contextlib import contextmanager

import pymysql

class_name = "SQLTool"
logger = LogController.getLogger(class_name)

class SQLTool(object):
    def __init__(self):
        pass

    @staticmethod
    def ConnectAndExecute(sqlconfig, sqlscript, **kwargs):
        '''
        连接到数据库并执行脚本

        :参数:
        
        * testcase ： testcase 实例
        * caseparam : 执行的 case 中对应的 脚本名称
        '''
        func_obj = None
        data = None
        try:
            sqlconfig = sqlconfig
            if sqlconfig.protocol == "mysql":
                func_obj = MysqlTool()
            elif sqlconfig.protocol == "sqlserver":
                func_obj = SqlServerTool()
            elif sqlconfig.protocol == "redis":
                func_obj = RedisTool()
            elif sqlconfig.protocol == "neo4j":
                func_obj = Neo4j()
            
            data = func_obj.ConnectAndExecute(sqlconfig, sqlscript, ** kwargs)
            return data
        except Exception as e:
            logger.log_print("debug", e)
        finally:
            logger.log_print("debug", func_obj)
            if func_obj is not None:
                func_obj.close()

