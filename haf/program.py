# encoding='utf-8'

'''
# program.py
# main program
'''

import logging
import os
import time
from multiprocessing import Process
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
from haf.utils import Utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
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
            loader = Loader(bus_client, self.args)
            loader.start()
            time.sleep(0.1)

    def _start_runner(self, count: int, log_dir: str, bus_client: BusClient):
        '''
        _start_runner : start runner (count)
        :param count: runner count
        :param log_dir: log
        :return:
        '''
        for x in range(count):
            runner = Runner(log_dir, bus_client, self.args)
            runner.start()
        time.sleep(0.5)

    def _start_recorder(self, bus_client: BusClient, sql_config: SQLConfig=None, sql_publish: bool=False, count: int=1, report_path: str="", log_dir: str=""):
        recorder = Recorder(bus_client, sql_config, sql_publish, count, report_path, self.case_name, log_dir, self.args.report_template, self.args)
        recorder.start()
        time.sleep(0.1)

    def _init_logging_module(self, args):
        logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        pass

    def _init_system_logger(self, log_dir: str, bus_client: BusClient):
        log = Logger(self.case_name, log_dir, bus_client, self.args)
        log.start()
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
        elif args.bus_server_port:
            self.bus_client = BusClient(None, args.bus_server_port, None)
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
            try:
                from hafapiserver.app import web_server
                ws = Process(target=web_server, args=(self.bus_client,), daemon=True)
                ws.start()
            except Exception as e:
                logger.error("Plugin hafapiserver is not installed, using 'pip install hafapiserver -U' to install")
                logger.error(e)

    def run(self, args):
        try:
            self.args = args
            self._init_logging_module(args)
            self.case_name = Utils.get_case_name(self.args.name)
            runner_count = args.runner_count if args.runner_count else 1
            self.only_bus(args)

            self._start_bus(local=args.bus_server if args.bus_server else False)

            self._bus_client(args)

            self._init_system_lock(args)
            self._init_system_logger(args.log_dir, self.bus_client)

            # only : module
            if args.only_loader:
                self._start_loader(1, self.bus_client)
            elif args.only_runner:
                self._start_runner(runner_count, f"{args.log_dir}/{self.case_name}", self.bus_client)
            elif args.only_recorder:
                self._start_recorder(self.bus_client, args.sql_publish_db, args.sql_publish, runner_count, args.report_output_dir, f"{args.log_dir}/{self.case_name}")
            else:
                self._start_loader(1, self.bus_client)
                self._start_runner(runner_count, f"{args.log_dir}/{self.case_name}", self.bus_client)
                self._start_recorder(self.bus_client, args.sql_publish_db, args.sql_publish, runner_count, args.report_output_dir, f"{args.log_dir}/{self.case_name}")
            
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
        else:
            logger.info("not only bus mode")

    def only_loader(self, args):
        if args.only_loader:
            pass

    def wait_end_signal(self, args):
        try:
            system_signal = self.bus_client.get_system()
            while True:
                if not args.web_server:
                    if not system_signal.empty():
                        self.signal = system_signal.get()
                        if self.signal == SIGNAL_RECORD_END or self.signal == SIGNAL_STOP:
                            logger.info("main -- stop")
                            
                            system_signal.put(SIGNAL_BUS_END)
                            break
                    time.sleep(0.1)
                else:
                    cmd = input(f"haf-{PLATFORM_VERSION}# ")
                    if self._run_cmd(cmd):
                        break
            time.sleep(1)
        except KeyboardInterrupt as key_inter:
            self.bus_client.get_param().put(SIGNAL_STOP)

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
        else:
            print("unsupported command!")
            result = self._help()
        return result

    def _rerun(self):
        case_handler = self.bus_client.get_case()
        while not case_handler.empty():
            case_handler.get()
        self._start_runner(self.args.runner_count if self.args.runner_count else 1, f"{self.args.log_dir}/{self.case_name}", self.bus_client)
        self._start_loader(1, self.bus_client)
        self._start_recorder(self.bus_client, self.args.sql_publish_db, self.args.sql_publish,self.args.runner_count, self.args.report_output_dir, f"{self.args.log_dir}/{self.case_name}")
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

    def _summary(help):
        pass

    def _case_name(self):
        print(self.case_name)
        return False

    def _exit(self):
        logger.info("main -- stop, wait for bus end")
        print(BANNER_STRS_EXIT)
        return True