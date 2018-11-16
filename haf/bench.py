# encoding='utf-8'

from haf.config import  *


class BaseBench(object):
    '''
    BaseCase the base of cases
    '''
    def __init__(self):
        self.name = None
        pass


class HttpApiBench(BaseBench):
    def __init__(self):
        super().__init__()
        self.name = None
