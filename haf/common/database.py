# encoding='utf-8'

from haf.common.log import Log
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

    def deserialize(self):
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
        import pymysql
        key = kwargs.get("key", "database$%common$%")
        commit = kwargs.get("commit", False)
        run_background = kwargs.get("run_background", False)
        logger.debug(sqlconfig)
        logger.debug(sqlconfig.deserialize() if sqlconfig else None)
        sqlconfig = sqlconfig
        self.connect_msql = None

        try:

            if "dictcursor" in kwargs.keys() and kwargs.get("dictcursor") is True:
                self.connect_msql = pymysql.connect(host=sqlconfig.host, port=sqlconfig.port, user=sqlconfig.username,
                                                    passwd=sqlconfig.password, db=sqlconfig.database,
                                                    cursorclass=pymysql.cursors.DictCursor)
            else:
                self.connect_msql = pymysql.connect(host=sqlconfig.host, port=sqlconfig.port, user=sqlconfig.username, passwd=sqlconfig.password, db=sqlconfig.database)
            cursor_m = self.connect_msql.cursor()
            data = []
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    if ss != None and ss != "None" and len(ss) > 5:
                        if not run_background:
                            logger.info(f"{key} start {sqlconfig.host} execute {ss}", __name__)
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        if not run_background:
                            logger.info(f"{key} result {str(data)}", __name__)
                    if isinstance(ss, tuple):
                        if not run_background:
                            logger.info(f"{key} tuple start {sqlconfig.host} execute {ss}", __name__)
                        cursor_m.execute(ss[0], ss[1])
                        data.append(cursor_m.fetchall())
                        if not run_background:
                            logger.info(f"{key} result {str(data)}", __name__)

            elif isinstance(sqlscript, str):
                if sqlscript != None and sqlscript != "None" and "None" not in sqlscript and len(sqlscript) > 5:
                    if not run_background:
                        logger.info(f"{key} start {sqlconfig.host} execute {sqlscript}", __name__)
                    cursor_m.execute(sqlscript)
                    data.append(cursor_m.fetchall())
                    if not run_background:
                        logger.info(f"{key} result {str(data)}", __name__)
                
            elif isinstance(sqlscript, tuple):
                if not run_background:
                    logger.info(f"{key} start {sqlconfig.host} execute {sqlscript}", __name__)
                cursor_m.execute(*sqlscript)
                data.append(cursor_m.fetchall())
                if not run_background:
                    logger.info(f"{key} result {str(data)}", __name__)

            if commit:
                self.connect_msql.commit()
            return data
        except Exception as e:
            logger.error(str(e), __name__)
            if self.connect_msql.open:
                self.connect_msql.close()
            return []

    def close(self):
        try:
            import pymysql
            if self.connect_msql is not None:
                self.connect_msql.close()
        except Exception as e:
            logger.error(e, __name__)


class SqlServerTool(object):
    '''
    SqlServerTool 工具类
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
        import pymssql
        key = kwargs.get("key", "database$%common$%")

        sqlconfig = sqlconfig
        self.connect_msql = None
        try:
            if "dictcursor" in kwargs.keys() and kwargs.get("dictcursor") is True:
                self.connect_msql = pymssql.connect(sqlconfig.host, sqlconfig.username, sqlconfig.password,
                                                sqlconfig.database)
            else:
                self.connect_msql = pymssql.connect(sqlconfig.host, sqlconfig.username, sqlconfig.password,
                                                sqlconfig.database)
            cursor_m = self.connect_msql.cursor()
            data = []
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    if ss != None and ss != "None" and "None" not in ss and len(ss) > 5:
                        logger.info(f"{key} [{sqlconfig.host}] start execute {ss}", __name__)
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        logger.info(f"{key} result {str(data)}", __name__)
            elif isinstance(sqlscript, str):
                if sqlscript != None and sqlscript != "None" and "None" not in sqlscript and len(sqlscript) > 5:
                    logger.info(f"{key} start [{sqlconfig.host}] execute {sqlscript}", __name__)
                    cursor_m.execute(sqlscript)
                    data.append(cursor_m.fetchall())
                    logger.info(f"{key} result {str(data)}", __name__)

            return data
        except Exception as e:
            logger.error(str(e), __name__)
            if self.connect_msql.open:
                self.connect_msql.close()
            return []

    def close(self):
        import pymssql
        if self.connect_msql is not None:
            self.connect_msql.close()


class RedisTool(object):
    '''
    Redis  工具类
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "RedisTool"

    def connect_execute(self, sqlconfig: SQLConfig, sqlscript: list, **kwargs):
        '''
        连接到数据库并执行脚本
        :参数:
        
        * testcase ： testcase 实例
        * caseparam : 执行的 case 中对应的 脚本名称
        '''
        
        import redis
        key = kwargs.get("key", "database$%common$%")
        commit = kwargs.get("commit", False)
        run_background = kwargs.get("run_background", False)

        sqlconfig = sqlconfig
        self.connect_redis = None

        try:
            self.connect_redis = redis.Redis(host=sqlconfig.host, port=sqlconfig.port, db=sqlconfig.database)
            logger.info(f"{key} start {sqlconfig.host} : [{self.connect_redis.type(sqlscript)}] execute {sqlscript}", __name__)
            if "zset" in str(self.connect_redis.type(sqlscript)):
                start = kwargs["start"]
                end = kwargs["end"]
                if "rev" in kwargs:
                    return self.connect_redis.zrevrange(sqlscript, start, end)
                else:
                    return self.connect_redis.zrange(sqlscript, start, end)
            elif "hash" in str(self.connect_redis.type(sqlscript)):
                return self.connect_redis.hget(sqlscript)
            else:
                return self.connect_redis.get(sqlscript)

        except Exception as e:
            logger.error(f"{key} {e}")

    def close(self):
        if self.connect_redis is not None:
            self.connect_redis.close()