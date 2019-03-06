# -*- encoding:utf-8 -*-

import logging

from haf.busclient import BusClient
from haf.common.sigleton import SingletonType


class BaseLogger(metaclass=SingletonType):

    def __init__(self, logger_name):
        self.logger_name = logger_name
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s <%(process)d> [%(name)s] %(message)s')
        self.logger = logging.getLogger(self.logger_name)
        self.bus_client = None

    def bind_busclient(self, bus_client: BusClient):
        self.bus_client = BusClient(bus_client.domain, bus_client.port, bus_client.auth_key)

    def debug(self, msg):
        self.msg_write(str(msg))
        #self.logger.debug(msg)

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
        if self.bus_client is None:
            self.bus_client = BusClient()
        self.bus_client.get_log().put(msg)


class Log:
    @staticmethod
    def getLogger(logger_name):
        logger = BaseLogger(logger_name)
        return logger

