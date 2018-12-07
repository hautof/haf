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
from haf.utils import Utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s <%(process)d> [%(name)s] %(message)s')
logger = logging.getLogger(__name__)


class Program(object):
    def __init__(self):
        self.bus_client = None
        self.case_name = ""

    def _start_bus(self, local=True):
        if local:
            pass
        else:
            self.bus_server = BusServer()
            self.bus_server.start()
            time.sleep(1)

    def _start_loader(self, count, bus_client):
        for x in range(count):
            loader = Loader(bus_client)
            loader.start()
            time.sleep(0.1)

    def _start_runner(self, count, log_dir: str):
        for x in range(count):
            runner = Runner(log_dir)
            runner.start()
        time.sleep(0.5)

    def _start_recorder(self, count: int=1, report_path: str=""):
        recorder = Recorder(count, report_path, self.case_name)
        recorder.start()
        time.sleep(0.1)

    def _init_logging_module(self, args):
        logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG, format='%(asctime)s %(levelname)s <%(process)d> [%(name)s] %(message)s')

    def _init_system_logger(self, log_dir: str, bus_client:BusClient):
        l = Logger(self.case_name, log_dir, bus_client)
        l.start()
        time.sleep(0.1)

    def _init_system_lock(self, args):
        if args.bus_server:
            return
        self.bus_client.get_lock().put(Lock)
        self.bus_client.get_web_lock().put(Lock)
        self.bus_client.get_case_lock().put(Lock)

    def _bus_client(self, args):
        if isinstance(args.bus_server, list):
            self.bus_client = BusClient(args.bus_server[1], args.bus_server[2], args.bus_server[0])
        else:
            self.bus_client = BusClient()

    def start_main(self):
        self.bus_client.get_param().put(SIGNAL_START)

    def stop_main(self):
        self.bus_client.get_param().put(SIGNAL_STOP)

    def put_loader_msg(self, args):
        if args.case:
            for arg in args.case:
                self.bus_client.get_param().put({"file_name": arg})

    def _start_web_server(self, args):
        if args.web_server:
            ws = Process(target=web_server)
            ws.start()

    def run(self, args):
        try:
            self._init_logging_module(args)
            self.case_name = Utils.get_case_name()
            runner_count = args.runner_count if args.runner_count else 1
            self.only_bus(args)

            self._start_bus(local=args.bus_server if args.bus_server else False)

            self._bus_client(args)

            self._init_system_logger(args.log_dir, self.bus_client)
            self._init_system_lock(args)

            if args.only_loader:
                self._start_loader(1, self.bus_client)
            elif args.only_runner:
                self._start_runner(runner_count, f"{args.log_dir}/{self.case_name}")
            elif args.only_recorder:
                self._start_recorder(runner_count, args.report_output_dir)
            else:
                self._start_loader(1, self.bus_client)
                self._start_runner(runner_count, f"{args.log_dir}/{self.case_name}")
                self._start_recorder(runner_count, args.report_output_dir)

            self.start_main()
            self.put_loader_msg(args)
            self.stop_main()
            self._start_web_server(args)

            self.wait_end_signal(args)
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

    def only_bus(self, args):
        if args.only_bus:
            self._start_bus(local=args.bus_server if args.bus_server else False)
            self._bus_client(args)
            self._init_system_lock(args)
            while True:
                time.sleep(1)

    def only_loader(self, args):
        if args.only_loader:
            pass

    def wait_end_signal(self, args):
        try:
            while True:
                if not args.web_server:
                    system_signal = self.bus_client.get_system()
                    signal = system_signal.get()
                    if signal == SIGNAL_RECORD_END or signal == SIGNAL_STOP:
                        logger.info("main -- stop")
                        self.bus_client.get_system().put(SIGNAL_BUS_END)
                        break
                    time.sleep(0.1)
            time.sleep(1)
        except KeyboardInterrupt as key_inter:
            self.bus_client.get_param().put(SIGNAL_STOP)


