#encoding='utf-8'

'''
# BusClient
'''

import logging
from multiprocessing.managers import BaseManager
from haf.config import *
from haf.common.sigleton import SingletonType
from haf.message import InfoManager

logger = logging.getLogger(__name__)


class BusClient(metaclass=SingletonType):
    '''
    bus client, using to connect to the bus server with host,port,auth_key
    '''
    def __init__(self, domain:str=None, port:str=None, auth_key:str=None):
        self.domain = BUS_CLIENT_DOMAIN if domain is None else domain
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
        InfoManager.register("get_publish_result")
        InfoManager.register("get_publish_runner")
        InfoManager.register("get_publish_loader")
        InfoManager.register("get_case_back")
        InfoManager.register("get_case_count")
        InfoManager.register("get_case_result_main")
        InfoManager.register("get_logger_end")
        # connect to the bus
        self.info_manager = InfoManager(address=(self.domain, self.port), authkey=self.auth_key)
        self.info_manager.connect()

    def get_case(self):
        '''
        get case, from loader to runner
        :return:
        '''
        return self.info_manager.get_case()

    def get_param(self):
        '''
        get param, from main to loader
        :return:
        '''
        return self.info_manager.get_param()

    def get_result(self):
        '''
        get result, from runner to recorder
        :return:
        '''
        return self.info_manager.get_result()

    def get_bench(self):
        '''
        no use yet !
        # TODO : remove useless
        :return:
        '''
        return self.info_manager.get_bench()

    def get_system(self):
        '''
        get system signal, from program to program
        :return:
        '''
        return self.info_manager.get_system()

    def get_log(self):
        '''
        get log, from loader, runner, recorder -> logger
        :return:
        '''
        return self.info_manager.get_log()

    def get_publish_result(self):
        '''
        get publish, from recorder to report
        :return:
        '''
        return self.info_manager.get_publish_result()

    def get_publish_loader(self):
        '''
        get publish, from loader to report
        :return:
        '''
        return self.info_manager.get_publish_loader()

    def get_publish_runner(self):
        '''
        get publish, from runner to report
        :return:
        '''
        return self.info_manager.get_publish_runner()

    def get_case_back(self):
        '''
        get case, from runner to loader
        :return:
        '''
        return self.info_manager.get_case_back()

    def get_case_count(self):
        '''
        get case count, from recorder to loader, check the case run over
        :return:
        '''
        return self.info_manager.get_case_count()

    def get_case_result_main(self):
        '''
        get case result main, using to the summary in program.py
        :return:
        '''
        return self.info_manager.get_case_result_main()
      
    def get_logger_end(self):
        '''
        '''
        return self.info_manager.get_logger_end()

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)