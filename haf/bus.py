# encoding='utf-8'

'''
# bus.py
# system bus, using to transfer message from service to service
#
'''
import time
from multiprocessing.managers import BaseManager
from queue import Queue
from multiprocessing import Process
from haf.config import BUS_DOMAIN, BUS_PORT, BUS_AUTH_KEY, SIGNAL_STOP, SIGNAL_BUS_END
from haf.message import MessageDict
from haf.log import Log

logger = Log.getLogger(__name__)


class InfoManager(BaseManager): pass
'''
# InfoManager
#
'''


class BusServer(Process):
    '''
    #　BusServer
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
        case = Queue()
        param = Queue()
        result = Queue()
        bench = MessageDict()
        system = Queue()
        InfoManager.register("get_case", callable=lambda: case)
        InfoManager.register("get_param", callable=lambda: param)
        InfoManager.register("get_result", callable=lambda: result)
        InfoManager.register("get_bench", callable=lambda: bench)
        InfoManager.register("get_system", callable=lambda: system)
        self.queue_manager = InfoManager(address=('', self.port), authkey=self.auth_key)
        self.server = self.queue_manager.get_server()

    def run(self):
        logger.debug("start Bus {}".format(self.pid))
        self.start_manager_server()
        self.server.serve_forever()
        while True:
            system_signal = self.queue_manager.get_system()
            if system_signal.get() == SIGNAL_BUS_END:
                self.stop()
                break
            time.sleep(0.1)


    def stop(self):
        logger.debug("end bus {}".format(self.pid))
        self.server.shutdown()
        self.is_stop = True





