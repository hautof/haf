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
from haf.config import *
from haf.common.exception import *

logger = logging.getLogger(__name__)


class Program(object):
    def __init__(self):
        pass

    def _start_bus(self):
       self.bus_server = BusServer()
       self.bus_server.start()
       time.sleep(0.1)

    def _start_loader(self, count):
        for x in range(count):
            loader = Loader()
            loader.start()
            time.sleep(0.1)

    def _start_runner(self, count):
        for x in range(count):
            runner = Runner()
            runner.start()
        time.sleep(0.5)

    def _start_recorder(self, count):
        for x in range(count):
            recorder = Recorder()
            recorder.start()
            time.sleep(0.1)


    def run(self):
        try:
            self._start_bus()
            self._start_loader(1)
            self._start_runner(2)
            self._start_recorder(1)
            bus_client = BusClient()
            bus_client.get_param().put(SIGNAL_START)
            bus_client.get_param().put({"file_name":"D:\workspace\mine\python\haf/testcases/CorpusApiTestTOEFL.xlsx"})
            bus_client.get_param().put(SIGNAL_STOP)
            while True:
                system_signal = bus_client.get_system()
                signal = system_signal.get()
                if signal == SIGNAL_RECORD_END or signal == SIGNAL_STOP:
                    logger.info("{} -- {}".format("main", "stop"))
                    bus_client.get_system().put(SIGNAL_BUS_END)
                    break
                time.sleep(0.1)
            time.sleep(1)

        except KeyboardInterrupt as key_inter:
            logger.error(key_inter)
        except FailLoaderException as loader_inter:
            logger.error(loader_inter)
        except FailRecorderException as recorder_inter:
            logger.error(recorder_inter)
        except FailRunnerException as runner_inter:
            logger.error(runner_inter)
        except FailFrameworkException as frame_inter:
            logger.error(frame_inter)






