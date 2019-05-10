# encoding='utf-8'

'''
# program.py
# main program
'''

import logging
import os
import time
from multiprocessing import Process, Lock as m_lock

from haf.result import HttpApiResult, AppResult, WebResult, EndResult

from haf.bus import BusServer
from haf.busclient import BusClient
from haf.common.database import SQLConfig
from haf.common.lock import Lock
from haf.config import *
from haf.common.exception import *
from haf.helper import Helper
from haf.loader import Loader
from haf.logger import Logger
from haf.recorder import Recorder
from haf.runner import Runner
from haf.signal import Signal
from haf.utils import Utils
from haf.pluginmanager import PluginManager, plugin_manager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


class Program(object):
    def __init__(self):
        self.bus_client = None
        self.case_name = ""

    def _start_bus(self, local=True):
        '''
        _start_bus : start bus server with default config
        :param local: bool, default is True
        :return: None
        '''
        if local:
            return
        elif self.args.bus_server_port:
            self.bus_server = BusServer(self.args.bus_server_port)
        else:
            self.bus_server = BusServer()
        self.bus_server.start()
        time.sleep(0.5)

    def _start_loader(self, count: int, bus_client: BusClient):
        '''
        _start_loader : start loader (count)
        :param count: loader count
        :param bus_client: bus client -> BusClient (connect to bus server)
        :return: None
        '''
        for x in range(count):
            loader = Loader(bus_client, self.loader_recorder_lock, self.args)
            loader.start()

    def _start_runner(self, count: int, log_dir: str, bus_client: BusClient):
        '''
        _start_runner : start runner (count)
        :param count: runner count
        :param log_dir: log
        :return:
        '''
        for x in range(count):
            runner = Runner(log_dir, bus_client, self.multi_process_locks, self.args)
            runner.start()

    def _start_recorder(self, bus_client: BusClient, count: int=1, log_dir: str="", time_str: str=""):
        '''
        start recorder
        :param bus_client:
        :param count:
        :param log_dir:
        :param time_str:
        :return:
        '''
        recorder = Recorder(bus_client, count, self.case_name, time_str, log_dir, self.args.report_template, self.loader_recorder_lock, self.args)
        recorder.start()

    def _init_logging_module(self, args):
        '''
        init logging module
        :param args:
        :return:
        '''
        logging.basicConfig(level=logging.DEBUG if not args.debug else logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        pass

    def _init_system_logger(self, log_dir: str, bus_client: BusClient):
        '''
        init system logger
        :param log_dir:
        :param bus_client:
        :return:
        '''
        log = Logger(self.case_name, self.time_str, log_dir, bus_client, self.args)
        log.start()

    def _init_system_lock(self, args):
        '''
        generate some locker
        :param args:
        :return:
        '''
        self.loader_recorder_lock = m_lock()
        self.multi_process_locks = [m_lock() for x in range(4)]
        if self.bus_client.get_case_count().empty():
            self.bus_client.get_case_count().put(0)

    def _bus_client(self, args):
        '''
        init bus client
        :param args:
        :return:
        '''
        if isinstance(args.bus_server, list):
            self.bus_client = BusClient(args.bus_server[1], args.bus_server[2], args.bus_server[0])
        elif args.bus_server_port:
            self.bus_client = BusClient(None, args.bus_server_port, None)
        else:
            self.bus_client = BusClient()
        self.params_loader = self.bus_client.get_param()

    def start_main(self):
        self.params_loader.put(Signal("main", SIGNAL_START))

    def stop_main(self):
        self.params_loader.put(Signal("main", SIGNAL_STOP))

    def put_loader_msg(self, args):
        if args.case:
            for arg in args.case:
                self.params_loader.put({"file_name": arg})

    def _start_web_server(self, args):
        plugin_manager.start_web_server(args, self.bus_client)

    def run(self, args):
        try:
            self.args = args
            self._init_logging_module(args)
            self.case_name = self.args.name
            self.time_str = Utils.get_time_str()
            self.case_log_dir = f"{args.log_dir}/{self.case_name}/{self.time_str}"
            self.runner_count = args.runner_count if args.runner_count else 1
            
            self.only_bus(args)

            self._start_bus(local=args.bus_server if args.bus_server else False)
            self._bus_client(args)
            self._init_system_lock(args)
            # this only in server bus
            if not args.bus_server:
                self._init_system_logger(args.log_dir, self.bus_client)

            # only : module
            if args.only_loader:
                self._start_loader(1, self.bus_client)
            elif args.only_runner:
                self._start_runner(self.runner_count, self.case_log_dir, self.bus_client)
            elif args.only_recorder:
                self._start_recorder(self.bus_client, self.runner_count, self.case_log_dir, self.time_str)
            else:
                self._start_loader(1, self.bus_client)
                self._start_runner(self.runner_count, self.case_log_dir, self.bus_client)
                self._start_recorder(self.bus_client, self.runner_count, self.case_log_dir, self.time_str)
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
            self._init_system_logger(args.log_dir, self.bus_client)
            self._start_recorder(self.bus_client, self.runner_count, self.case_log_dir, self.time_str)
            self.wait_end_signal(args)
            sys.exit(0)
        else:
            logger.info("not only bus mode")

    def only_loader(self, args):
        if args.only_loader:
            pass

    def wait_end_signal(self, args):
        try:
            time.sleep(2)
            system_signal = self.bus_client.get_system()
            while True:
                if not args.console:
                    if not system_signal.empty():
                        self.signal = system_signal.get()
                        signal = self.signal.signal if isinstance(self.signal, Signal) else None
                        logger.info(f"program signal {SIGNAL_GROUP.get(signal) if signal in [x for x in range(20, 30)] else None}")
                        # check the end signal from recorder to main
                        if signal == SIGNAL_RECORD_END or signal == SIGNAL_STOP:
                            if not args.local_logger:
                                while True:
                                  if not system_signal.empty():
                                      signal_logger = system_signal.get()
                                      signal_logger = signal_logger.signal if isinstance(signal_logger, Signal) else None
                                      logger.info(f"program signal {SIGNAL_GROUP.get(signal_logger) if signal_logger in [x for x in range(20, 30)] else None}")
                                      # check the logger signal from logger to main
                                      if signal_logger == SIGNAL_LOGGER_END:
                                          logger.info("main -- stop")
                                          system_signal.put(Signal("main", SIGNAL_RECORD_END))
                                          system_signal.put(Signal("main", SIGNAL_LOGGER_END))
                                          break
                            # if use local logger, just end the main program
                            else:
                                logger.info("main -- stop")
                                system_signal.put(Signal("main", SIGNAL_RECORD_END))
                                system_signal.put(Signal("main", SIGNAL_LOGGER_END))
                            break
                    time.sleep(0.1)
                else:
                    cmd = input(f"haf-{PLATFORM_VERSION}# ")
                    if self._run_cmd(cmd):
                        break
            if args.only_bus:
                logger.info("main - wait for other process end !")
                time.sleep(3)
            time.sleep(0.1)
        except KeyboardInterrupt as key_inter:
            self.params_loader.put(Signal("main", SIGNAL_STOP))

    # TODO: Here need CMDER to support cmd command ...
    def _run_cmd(self, cmd):
        if cmd == "rerun" or cmd == "r":
            result = self._rerun()
        elif cmd == "version" or cmd == "v":
            result = self._version()
        elif cmd == "help" or cmd == "h":
            result = self._help()
        elif cmd == "name" or cmd == "n":
            result = self._case_name()
        elif cmd == "exit" or cmd == "e":
            result = self._exit()
        elif cmd == "summary" or cmd == "s":
            result = self._summary()
        else:
            print("unsupported command!")
            result = self._help()
        return result

    def _rerun(self):
        case_handler = self.bus_client.get_case()
        while not case_handler.empty():
            case_handler.get()
        self._start_runner(self.args.runner_count if self.args.runner_count else 1, self.case_log_dir, self.bus_client)
        self._start_loader(1, self.bus_client)
        self._start_recorder(self.bus_client, self.runner_count, self.case_log_dir, self.time_str)
        self.start_main()
        self.put_loader_msg(self.args)
        self.stop_main()
        return False

    def _version(self):
        print(BANNER_STRS)
        return False

    def _help(self):
        help = f"""
haf-{PLATFORM_VERSION}#
# rerun   / r     rerun the input cases
# version / v     version of haf
# help    / h     help information
# name    / n     case name of this test
# summary / s     summary of this test
# exit    / e     exit 
        """
        print(help)
        return False

    def _summary(self):
        result_main = self.bus_client.get_case_result_main()
        if not result_main.empty():
            results = result_main.get()
            if isinstance(results, EndResult):
                self.results = results
        if hasattr(self, "results") and isinstance(self.results, EndResult):
            pass
        else:
            self.results = EndResult()
        result_summary = "|{:^8}|{:^8}|{:^8}|{:^8}|{:^8}|{:^25}|{:^25}|".format(self.results.passed, self.results.failed, self.results.skip, \
                        self.results.error, self.results.all, self.results.begin_time, self.results.end_time)
        print("--------------------------------------------------------------------------------------------------")
        print("|--\33[32mPASS\33[0m--|--\33[31mFAIL\33[0m--|--\33[37mSKIP\33[0m--|--\33[35mERROR\33[0m-|---\33[36mALL\33[0m--|----------\33[36mBegin\33[0m----------|-----------\33[36mEnd\33[0m-----------|")
        print(result_summary)
        print("--------------------------------------------------------------------------------------------------")

    def _case_name(self):
        print(self.case_name)
        return False

    def _exit(self):
        logger.info("main -- stop, wait for bus end")
        print(BANNER_STRS_EXIT)
        return True