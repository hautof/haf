# encoding='utf-8'

'''
# bus.py
# system bus, using to transfer message from service to service
#
'''
from multiprocessing.managers import BaseManager
from queue import Queue
from multiprocessing import Process
from haf.config import BUS_DOMAIN, BUS_PORT, BUS_AUTH_KEY
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
        InfoManager.register("get_case", callable=lambda: case)
        InfoManager.register("get_param", callable=lambda: param)
        InfoManager.register("get_result", callable=lambda: result)
        InfoManager.register("get_bench", callable=lambda: bench)
        self.queue_manager = InfoManager(address=('', self.port), authkey=self.auth_key)
        self.server = self.queue_manager.get_server()

    def run(self):
        logger.debug("start Bus {}".format(self.pid))
        self.start_manager_server()
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.is_stop = True





