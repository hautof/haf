import os, sys, time, json

sys.path.append("..\..\..")

from haf.pylib.Log.LogController import LogController
from haf.pylib.SQL.SQLConfig import SQLConfig

import redis

class_name = "RedisTool"
logger = LogController.getLogger(class_name)


class RedisTool(object):
    '''
    Redis  工具类
    '''
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
        connect_redis = None
        logger.log_print("info", "start connect to {}".format(str(sqlconfig.host)), "ConnectAndExecute")
        try:
            connect_redis = redis.Redis(host=sqlconfig.host, port=sqlconfig.port, db=sqlconfig.database)
            logger.log_print("info", "type is {}".format(str(connect_redis.type(sqlscript))), "ConnectAndExecute")
            if "zset" in str(connect_redis.type(sqlscript)):
                start = kwargs["start"]
                end = kwargs["end"]
                if "rev" in kwargs:
                    return connect_redis.zrevrange(sqlscript, start, end)
                else:
                    return connect_redis.zrange(sqlscript, start, end)
            elif "hash" in str(connect_redis.type(sqlscript)):
                return connect_redis.hget(sqlscript)
            else:
                return connect_redis.get(sqlscript)

        except Exception as e:
            logger.log_print("error", str(e), "ConnectAndExecute")

if __name__ == "__main__":
    sqlconfig = SQLConfig()
    sqlconfig.host = "192.168.41.230"
    sqlconfig.port = 6379
    sqlconfig.password = "123456"
    sqlconfig.database = "14"
    
    connect_redis = redis.Redis(host=sqlconfig.host, port=sqlconfig.port, db=sqlconfig.database)
    print(RedisTool.ConnectAndExecute(sqlconfig,"corpus:vocabulary:search:rank:2018-08-30", start=0, end=1, rev=True))