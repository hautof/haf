# encoding='utf-8'

'''
file name: database.py
description : database tool for haf, include MySQL,SQLServer,Redis
others :
all these tools need the arg : SQLConfig
    usage:
        sql_config = SQLConfig()
        sql_config.constructor(inputs)
    note:
        inputs is a dict type, include host, port, username, password, dtabase, protocol, id,  sql_name key
'''


from haf.common.log import Log
from contextlib import contextmanager

logger = Log.getLogger(__name__)


class SQLConfig(object):
    '''
    SQLConfig, the sql tool config
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
        using dict type to init the SQLConfig
        :param inputs
        :return None
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
        '''
        deserialize to an dict type
        :return: {} of SQLConfig
        '''
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
    MysqlTool
    '''
    def __init__(self):
        pass

    def connect_execute(self, sqlconfig: SQLConfig, sqlscript: list, **kwargs)-> tuple:
        '''
        connect and execute

        :param sqlconfig SQLConfig
        :param sqlscript the script of sql, can be string or list
        :param kwargs, include key of testcase, commit of sqlscript, run_background
        :return return the result of sql execute
        '''
        import pymysql
        key = kwargs.get("key", "database$%common$%")
        commit = kwargs.get("commit", False)
        run_background = kwargs.get("run_background", False)
        logger.debug(sqlconfig.deserialize() if sqlconfig else None, __name__)
        logger.debug(sqlscript, __name__)
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
            # here if sqlscript is list type, must execute every
            # script and append the result to the end_result
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    # valued sql script must not be None and length > 5
                    if ss != None and ss != "None" and len(ss) > 5:
                        if not run_background:
                            logger.info(f"{key} start {sqlconfig.host} execute {ss}", __name__)
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        if not run_background:
                            logger.info(f"{key} result {str(data)}", __name__)
                    # if sql script is tuple type, means to be 2 parts: 1 is the script, 2 is the parameter
                    if isinstance(ss, tuple) and len(ss)>2:
                        if not run_background:
                            logger.info(f"{key} tuple start {sqlconfig.host} execute {ss}", __name__)
                        cursor_m.execute(ss[0], ss[1])
                        data.append(cursor_m.fetchall())
                        if not run_background:
                            logger.info(f"{key} result {str(data)}", __name__)
            # if the sqlscript is the string type, can just run it
            elif isinstance(sqlscript, str):
                if sqlscript != None and sqlscript != "None" and "None" not in sqlscript and len(sqlscript) > 5:
                    if not run_background:
                        logger.info(f"{key} start {sqlconfig.host} execute {sqlscript}", __name__)
                    cursor_m.execute(sqlscript)
                    data.append(cursor_m.fetchall())
                    if not run_background:
                        logger.info(f"{key} result {str(data)}", __name__)
            # if the sqlscript is the tuple type and we do not know the length,
            # just execute the *sqlscript by cursor.execute()
            elif isinstance(sqlscript, tuple):
                if not run_background:
                    logger.info(f"{key} start {sqlconfig.host} execute {sqlscript}", __name__)
                cursor_m.execute(*sqlscript)
                data.append(cursor_m.fetchall())
                if not run_background:
                    logger.info(f"{key} result {str(data)}", __name__)
            # some sqlscript need commit to make it work, like update, delete, insert
            if commit:
                self.connect_msql.commit()
            logger.debug(data, __name__)
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
    SqlServerTool
    '''
    def __init__(self):
        pass

    def connect_execute(self, sqlconfig:SQLConfig, sqlscript:list, **kwargs):
        '''
        connect and execute

        :param sqlconfig SQLConfig
        :param sqlscript the script of sql, can be string or list
        :param kwargs, include key of testcase, commit of sqlscript, run_background
        :return return the result of sql execute
        '''
        import pymssql
        key = kwargs.get("key", "database$%common$%")
        commit = kwargs.get("commit", False)
        run_background = kwargs.get("run_background", False)
        logger.debug(sqlconfig.deserialize() if sqlconfig else None, __name__)
        logger.debug(sqlscript, __name__)
        sqlconfig = sqlconfig
        self.connect_msql = None

        try:

            if "dictcursor" in kwargs.keys() and kwargs.get("dictcursor") is True:
                self.connect_msql = pymssql.connect(host=sqlconfig.host, port=sqlconfig.port, user=sqlconfig.username,
                                                    password=sqlconfig.password, database=sqlconfig.database)
                cursor_m = self.connect_msql.cursor(as_dict=True)
            else:
                self.connect_msql = pymssql.connect(host=sqlconfig.host, port=sqlconfig.port, user=sqlconfig.username,
                                                    password=sqlconfig.password, database=sqlconfig.database)
                cursor_m = self.connect_msql.cursor()

            data = []
            # here if sqlscript is list type, must execute every
            # script and append the result to the end_result
            if isinstance(sqlscript, list):
                for ss in sqlscript:
                    # valued sql script must not be None and length > 5
                    if ss != None and ss != "None" and len(ss) > 5:
                        if not run_background:
                            logger.info(f"{key} start {sqlconfig.host} execute {ss}", __name__)
                        cursor_m.execute(ss)
                        data.append(cursor_m.fetchall())
                        if not run_background:
                            logger.info(f"{key} result {str(data)}", __name__)
                    # if sql script is tuple type, means to be 2 parts: 1 is the script, 2 is the parameter
                    if isinstance(ss, tuple) and len(ss) > 2:
                        if not run_background:
                            logger.info(f"{key} tuple start {sqlconfig.host} execute {ss}", __name__)
                        cursor_m.execute(ss[0], ss[1])
                        data.append(cursor_m.fetchall())
                        if not run_background:
                            logger.info(f"{key} result {str(data)}", __name__)
            # if the sqlscript is the string type, can just run it
            elif isinstance(sqlscript, str):
                if sqlscript != None and sqlscript != "None" and "None" not in sqlscript and len(sqlscript) > 5:
                    if not run_background:
                        logger.info(f"{key} start {sqlconfig.host} execute {sqlscript}", __name__)
                    cursor_m.execute(sqlscript)
                    data.append(cursor_m.fetchall())
                    if not run_background:
                        logger.info(f"{key} result {str(data)}", __name__)
            # if the sqlscript is the tuple type and we do not know the length,
            # just execute the *sqlscript by cursor.execute()
            elif isinstance(sqlscript, tuple):
                if not run_background:
                    logger.info(f"{key} start {sqlconfig.host} execute {sqlscript}", __name__)
                cursor_m.execute(*sqlscript)
                data.append(cursor_m.fetchall())
                if not run_background:
                    logger.info(f"{key} result {str(data)}", __name__)
            # some sqlscript need commit to make it work, like update, delete, insert
            if commit:
                self.connect_msql.commit()
            logger.debug(data, __name__)
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
    Redis
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "RedisTool"

    def connect_execute(self, sqlconfig: SQLConfig, sqlscript: list, **kwargs):
        '''
        connect and execute

        :param sqlconfig SQLConfig
        :param sqlscript the script of sql, can be string or list
        :param kwargs, include key of testcase, commit of sqlscript, run_background
        :return return the result of sql execute
        '''
        # TODO:
        # need extend like MysqlTool
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