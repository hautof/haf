#encoding='utf-8'


from haf.pylib.Log.LogController import LogController

from haf.pylib.SQL.MysqlTool import MysqlTool

from haf.pylib.SQL.SqlServerTool import SqlServerTool

from haf.pylib.SQL.RedisTool import RedisTool

from haf.pylib.SQL.Neo4jTool import Neo4j

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
        sqlconfig = sqlconfig
        if sqlconfig.protocol == "mysql":
            return MysqlTool.ConnectAndExecute(sqlconfig, sqlscript, **kwargs)
        elif sqlconfig.protocol == "sqlserver":
            return SqlServerTool.ConnectAndExecute(sqlconfig, sqlscript, **kwargs)
        elif sqlconfig.protocol == "redis":
            return RedisTool.ConnectAndExecute(sqlconfig, sqlscript, **kwargs)
        elif sqlconfig.protocol == "neo4j":
            return Neo4j.ConnectAndExecute(sqlconfig, sqlscript, ** kwargs)
