# encoding='utf-8'

'''
# bus.py
# system bus, using to transfer message from service to service
#
'''
import logging
import time
from multiprocessing.managers import BaseManager
from queue import Queue
from multiprocessing import Process, Pipe

from haf.common.exception import FailBusException
from haf.config import BUS_DOMAIN, BUS_PORT, BUS_AUTH_KEY, SIGNAL_BUS_END

logger = logging.getLogger(__name__)


class InfoManager(BaseManager): pass
'''
# InfoManager
#
'''


class BusServer(Process):
    '''
    # BusServer the bus server process
    '''
    def __init__(self):
        super().__init__()
        self.domain = BUS_DOMAIN
        self.port = BUS_PORT
        self.auth_key = BUS_AUTH_KEY
        self.queue_manager = None
        self.server = None
        self.is_stop = False
        self.daemon = True

    def start_manager_server(self):
        '''
        start manager server

        :return:
        '''
        # case queue, keep the case
        case = Queue(maxsize=-1)
        # param queue, keep the queue
        param = Queue(maxsize=-1)
        # result queue, keep the result
        result = Queue(maxsize=-1)
        # bench dict, keep the bench
        bench = Queue(maxsize=-1)
        # system queue, keep the signal of system
        system = Queue(maxsize=-1)
        # log queue
        log = Queue(maxsize=-1)
        # lock queue
        lock = Queue(maxsize=1)
        # web lock queue
        web_lock = Queue(maxsize=1)
        # case lock queue
        case_lock = Queue(maxsize=1)
        # result queue to web server
        publish_result = Queue(maxsize=1)
        # loader queue to web server
        publish_loader = Queue(maxsize=1)
        # runner queue to web server
        publish_runner = Queue(maxsize=1)

        # register the functions to InfoManager
        InfoManager.register("get_case", callable=lambda: case)
        InfoManager.register("get_param", callable=lambda: param)
        InfoManager.register("get_result", callable=lambda: result)
        InfoManager.register("get_bench", callable=lambda: bench)
        InfoManager.register("get_system", callable=lambda: system)
        InfoManager.register("get_log", callable=lambda: log)
        InfoManager.register("get_lock", callable=lambda: lock)
        InfoManager.register("get_web_lock", callable=lambda: web_lock)
        InfoManager.register("get_case_lock", callable=lambda: case_lock)
        InfoManager.register("get_publish_result", callable=lambda: publish_result)
        InfoManager.register("get_publish_runner", callable=lambda: publish_runner)
        InfoManager.register("get_publish_loader", callable=lambda: publish_loader)

        self.queue_manager = InfoManager(address=('', self.port), authkey=self.auth_key)
        self.server = self.queue_manager.get_server()

    def run(self):
        '''
        overwrite the run of Process
        :return:
        '''
        try:
            logger.info("start Bus {}".format(self.pid))
            self.start_manager_server()
            self.server.serve_forever()
            while True:
                system_signal = self.queue_manager.get_system()
                if system_signal.get() == SIGNAL_BUS_END:
                    self.stop()
                    break
                time.sleep(1)
        except Exception:
            raise FailBusException

    def stop(self):
        logger.info(f"end bus {self.pid}")
        self.server.shutdown()
        self.is_stop = True





