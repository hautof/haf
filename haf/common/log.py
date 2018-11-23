# -*- encoding:utf-8 -*-

import logging
from logging import handlers
import time

from haf.busclient import BusClient
from haf.common.sigleton import SingletonType


class BaseLogger(metaclass=SingletonType):

    def __init__(self, logger_name):
        self.logger_name = logger_name
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s <%(process)d> [%(name)s] %(message)s')
        self.logger = logging.getLogger(self.logger_name)
        #local_handler = logging.handlers.QueueHandler()

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.msg_write(str(msg))
        self.logger.info(msg)

    def warning(self, msg):
        self.msg_write(str(msg))
        self.logger.warning(msg)

    def error(self, msg):
        self.msg_write(str(msg))
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def msg_write(self, msg):
        bus_client = BusClient()
        log_queue = bus_client.get_log()
        log_queue.put(msg)


    @property
    def now(self):
        '''
        get datetime now to str
        :return: time now str
        '''
        current_time = time.time()
        local_time = time.localtime(current_time)
        time_temp = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        secs = (current_time - int(current_time)) * 1000
        timenow = "%s %03d" % (time_temp, secs)
        return timenow


class Log:
    @staticmethod
    def getLogger(logger_name):
        logger = BaseLogger(logger_name)
        return logger

