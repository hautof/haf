# encoding='utf-8'

'''
# program.py
# main program
'''

import logging
import time
from multiprocessing import Process

from haf.bus import BusServer
from haf.busclient import BusClient
from haf.common.lock import Lock
from haf.loader import Loader
from haf.recorder import Recorder
from haf.runner import Runner
from haf.config import *
from haf.common.exception import *
from haf.logger import Logger
from haf.ext.webserver.app import web_server

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s <%(process)d> [%(name)s] %(message)s')
logger = logging.getLogger(__name__)


class Program(object):
    def __init__(self):
        pass

    def _start_bus(self, local=True):
        if local:
           self.bus_server = BusServer()
           self.bus_server.start()
           time.sleep(1)

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

    def _init_system_logger(self):
        l = Logger()
        l.start()
        time.sleep(0.1)

    def _init_system_lock(self):
        self.bus_client.get_lock().put(Lock)
        self.bus_client.get_web_lock().put(Lock)

    def start_main(self, args):
        self.bus_client.get_param().put(SIGNAL_START)
        self._init_system_lock()

        self.bus_client.get_param().put({"file_name": args.case})
        if args.web_server:
            ws = Process(target=web_server)
            ws.start()
        else:
            self.bus_client.get_param().put(SIGNAL_STOP)

    def run(self, args):
        try:
            self._start_bus(local=True if not args.bus_server else False)
            self._init_system_logger()
            self._start_loader(1)
            self._start_runner(args.runner_count if args.runner_count else 1)
            self._start_recorder(1)
            self.bus_client = BusClient()
            self.start_main(args)
            self.wait_end_signal()
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



    def wait_end_signal(self):
        try:
            while True:
                system_signal = self.bus_client.get_system()
                signal = system_signal.get()
                if signal == SIGNAL_RECORD_END or signal == SIGNAL_STOP:
                    logger.info("main -- stop")
                    self.bus_client.get_system().put(SIGNAL_BUS_END)
                    break
                time.sleep(0.1)
            time.sleep(1)

        except KeyboardInterrupt as key_inter:
            #logger.error(key_inter)
            self.bus_client.get_param().put(SIGNAL_STOP)


