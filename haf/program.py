# encoding='utf-8'

'''
# program.py
# main program
'''

import logging
import time

from haf.bus import BusServer
from haf.busclient import BusClient
from haf.loader import Loader
from haf.recorder import Recorder
from haf.runner import Runner

logger = logging.getLogger(__name__)


class Program(object):
    def __init__(self):
        pass

    def _start_bus(self, count):
        for x in range(count):
            bus_server = BusServer()
            bus_server.start()

    def _start_loader(self, count):
        for x in range(count):
            loader = Loader()
            loader.start()

    def _start_runner(self, count):
        for x in range(count):
            runner = Runner()
            runner.start()

    def _start_recorder(self, count):
        for x in range(count):
            recorder = Recorder()
            recorder.start()

    def run(self):
        self._start_bus(1)
        self._start_loader(1)
        self._start_runner(2)
        self._start_recorder(1)
        bus_client = BusClient()
        bus_client.get_param().put("start")
        while True:
            time.sleep(1)







