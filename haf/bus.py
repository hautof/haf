# encoding='utf-8'

'''
# bus.py
# system bus, using to transfer message from service to service
#
'''


from queue import Queue
from multiprocessing import Process
from haf.config import BUS_DOMAIN, BUS_PORT, BUS_AUTH_KEY
from haf.message import InfoManager, MessageDict

import logging
logger = logging.getLogger(__name__)


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

    # register method to InfoManager
    def add_method(self):
        case = Queue()
        InfoManager.register("get_case", callable=lambda: case)
        param = Queue()
        InfoManager.register("get_param", callable=lambda: param)
        result = Queue()
        InfoManager.register("get_result", callable=lambda: result)
        bench = MessageDict()
        InfoManager.register("get_bench", callable=lambda: bench)

    def start_manager_server(self):
        case = Queue()
        InfoManager.register("get_case", callable=lambda: case)
        param = Queue()
        InfoManager.register("get_param", callable=lambda: param)
        result = Queue()
        InfoManager.register("get_result", callable=lambda: result)
        bench = MessageDict()
        InfoManager.register("get_bench", callable=lambda: bench)
        self.queue_manager = InfoManager(address=('', self.port), authkey=self.auth_key)
        self.server = self.queue_manager.get_server()

    def run(self):
        self.add_method()
        self.start_manager_server()
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.is_stop = True





