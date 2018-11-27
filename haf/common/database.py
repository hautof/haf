# encoding='utf-8'

from haf.common.log import Log
import pymysql
from contextlib import contextmanager

logger = Log.getLogger(__name__)


class SQLConfig(object):
    '''
    sql config
    '''

    def __init__(self):
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.database = None
        self.protocol = None
        self.id = None
        self.sqlname = None

    def constructor(self, inputs:dict={}):
        '''
        构造器
        '''
        self.host = str(inputs.get("host"))
        self.port = inputs.get("port")
        self.username = str(inputs.get("username"))
        self.password = str(inputs.get("password"))
        self.database = str(inputs.get("database"))
        self.protocol = str(inputs.get("protocol"))
        self.id = inputs.get("id")
        self.sqlname = str(inputs.get("sql_name"))

    def __str__(self):
        return {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "database": self.database,
            "protocol": self.protocol,
            "id": self.id,
            "sql_name": self.sqlname
        }


class MysqlTool(object):
    '''
    Mysql 工具类
    '''
    def __init__(self):
        pass

    def connect_execute(self, sqlconfig:SQLConfig, sqlscript:list, **kwargs):
        '''
        连接到数据库并执行脚本
        :参数:

        * sqlconfig ： sqlconfig 实例
        * sqlscript : 执行的 sqlscript
        '''
        key = kwargs.get("key", "database$%common$%")

        sqlconfig = sqlconfig
        self.connect_msql = None
        try:
            if "dictcursor" in kwargs.keys() and kwargs.get("dictcursor") is True:
                self.connect_msql = pymysql.connect(sqlconfig.host, sqlconfig.username, sqlconfig.password,
                                                sqlconfig.database, cursorclass = pymysql.cursors.DictCursor)
            else:
                self.connect_msql = pymysql.connect(sqlconfig.host, sqlconfig.username, sqlconfig.password,
                                                sqlconfig.database)
            cursor_m = self.connect_msql.cursor()
            data = []
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    if ss != None and ss != "None" and "None" not in ss and len(ss) > 5:
                        logger.info(f"{key} start execute {ss}")
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        logger.info(f"{key} result {str(data)}")
            elif isinstance(sqlscript, str):
                if sqlscript != None and sqlscript != "None" and "None" not in sqlscript and len(sqlscript) > 5:
                    logger.info(f"{key} start execute {sqlscript}")
                    cursor_m.execute(sqlscript)
                    data.append(cursor_m.fetchall())
                    logger.info(f"{key} result {str(data)}")

            return data
        except Exception as e:
            logger.error(str(e))
            if self.connect_msql.open:
                self.connect_msql.close()
            return []

    def close(self):
        if self.connect_msql is not None:
            self.connect_msql.close()

