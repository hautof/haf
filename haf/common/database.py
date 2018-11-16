# encoding='utf-8'

from sqlalchemy.dialects.mysql import pymysql
from haf.common.log import Log
import pymysql

logger = Log.getLogger(__name__)


class MysqlTool(object):
    '''
    Mysql 工具类
    '''
    def __init__(self):
        pass

    def connect_execute(self, sqlconfig, sqlscript, **kwargs):
        '''
        连接到数据库并执行脚本
        :参数:

        * sqlconfig ： sqlconfig 实例
        * sqlscript : 执行的 sqlscript
        '''

        sqlconfig = sqlconfig
        self.connect_msql = None
        try:
            self.connect_msql = pymysql.connect(sqlconfig.host, sqlconfig.username, sqlconfig.password,
                                                sqlconfig.database)
            cursor_m = self.connect_msql.cursor()
            data = []
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    if ss != None and ss != "None" and "None" not in ss and len(ss) > 5:
                        logger.log_print("info", "start execute {}".format(ss), "ConnectAndExecute")
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        logger.log_print("info", "result {}".format(str(data)), "ConnectAndExecute")
            return data
        except Exception as e:
            logger.log_print("error", str(e), "ConnectAndExecute")
            if self.connect_msql is not None:
                self.connect_msql.close()

    def close(self):
        if self.connect_msql is not None:
            self.connect_msql.close()

class SQLConfig(object):
    '''
    sql config 实体
    '''

    def __init__(self):
        self.class_name = "SQLConfig"
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.database = None
        self.protocol = None
        self.id = None
        self.sqlname = None

    def constructor(self, *args):
        '''
        构造器
        '''
        logger.log_print("info", "start", "constructor ")
        if len(args) > 0:
            if isinstance(args[0], dict):
                logger.log_print("info", str(args[0].get("host")), "constructor ")
                config = args[0]
                self.host = str(config.get("host"))
                self.port = config.get("port")
                self.username = str(config.get("username"))
                self.password = str(config.get("password"))
                self.database = str(config.get("database"))
                self.protocol = str(config.get("protocol"))
                self.id = config.get("id")
                self.sqlname = str(config.get("sql_name"))
        logger.log_print("info", "ok", "constructor ")