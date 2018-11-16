# encoding='utf-8'
import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.case import HttpApiCase


class Recorder(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True

    def run(self):
        self.bus_client = BusClient()
        while True:
            results = self.bus_client.get_result()
            if not results.empty() :
                result = results.get()
                print("recorder {} -- {}".format(self.pid, result))
            time.sleep(0.1)