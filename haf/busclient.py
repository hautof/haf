
'''
# BusClient
'''
from haf.config import BUS_DOMAIN, BUS_PORT, BUS_AUTH_KEY
from haf.message import InfoManager


class BusClient(object):
    def __init__(self):
        self.domain = BUS_DOMAIN
        self.port = BUS_PORT
        self.auth_key = BUS_AUTH_KEY
        self.queue = None
        self.add_method()
        self.info_manager = InfoManager(address=('127.0.0.1', self.port), authkey=self.auth_key)
        self.info_manager.connect()

    def add_method(self):
        InfoManager.register("get_param")
        InfoManager.register("get_case")
        InfoManager.register("get_result")
        InfoManager.register("get_bench")

    def get_case(self):
        return self.info_manager.get_case()

    def get_param(self):
        return self.info_manager.get_param()

    def get_result(self):
        return self.info_manager.get_result()

    def get_bench(self):
        return self.info_manager.get_bench()

