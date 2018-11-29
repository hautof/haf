#encoding='utf-8'

'''
# BusClient
'''
import contextlib
import logging
from multiprocessing.managers import BaseManager
from haf.config import *
from haf.common.sigleton import SingletonType

logger = logging.getLogger(__name__)


class InfoManager(BaseManager): pass

'''
# InfoManager
'''


class BusClient(metaclass=SingletonType):
    def __init__(self, domain:str=None, port:str=None, auth_key:str=None):
        self.domain = BUS_DOMAIN if domain is None else domain
        self.port = BUS_PORT if port is None else port
        self.auth_key = BUS_AUTH_KEY if auth_key is None else auth_key
        self.queue = None
        #register the functions to InfoManager
        InfoManager.register("get_param")
        InfoManager.register("get_case")
        InfoManager.register("get_result")
        InfoManager.register("get_bench")
        InfoManager.register("get_system")
        InfoManager.register("get_log")
        InfoManager.register("get_lock")
        InfoManager.register("get_web_lock")
        InfoManager.register("get_publish_result")
        InfoManager.register("get_publish_result")
        InfoManager.register("get_publish_runner")
        InfoManager.register("get_publish_loader")
        InfoManager.register("get_case_lock")
        # connect to the bus
        self.info_manager = InfoManager(address=('127.0.0.1', self.port), authkey=self.auth_key)
        self.info_manager.connect()

    def get_case(self):
        return self.info_manager.get_case()

    def get_param(self):
        return self.info_manager.get_param()

    def get_result(self):
        return self.info_manager.get_result()

    def get_bench(self):
        return self.info_manager.get_bench()

    def get_system(self):
        return self.info_manager.get_system()

    def get_log(self):
        return self.info_manager.get_log()

    def get_lock(self):
        return self.info_manager.get_lock()

    def get_web_lock(self):
        return self.info_manager.get_web_lock()

    def get_case_lock(self):
        return self.info_manager.get_case_lock()

    def get_publish_result(self):
        return self.info_manager.get_publish_result()

    def get_publish_loader(self):
        return self.info_manager.get_publish_loader()

    def get_publish_runner(self):
        return self.info_manager.get_publish_runner()