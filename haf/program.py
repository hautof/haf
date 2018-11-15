# encoding='utf-8'

'''
# program.py
# main program
'''

import logging
import time

from haf.bus import BusServer
from haf.loader import Loader
from haf.runner import Runner

logger = logging.getLogger(__name__)


class Program(object):
    def __init__(self):
        pass

    def _start_bus(self):
        bus_server = BusServer()
        bus_server.start()

    def _start_loader(self):
        loader = Loader()
        loader.start()

    def _start_runner(self):
        runner = Runner()
        runner.start()

    def run(self):
        self._start_bus()
        self._start_loader()
        self._start_runner()
        while True:
            time.sleep(1)







