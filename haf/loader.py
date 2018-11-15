# encoding='utf-8'
import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.case import HttpApiCase


class Loader(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True

    def run(self):
        self.bus_client = BusClient()
        while True:
            params = self.bus_client.get_param()
            if not params.empty() :
                param = params.get()
                print(param)
            case = self.bus_client.get_case()
            case.put(HttpApiCase())
            time.sleep(1)