# encoding='utf-8'

from haf.config import  *
from haf.result import BaseResult, HttpApiResult


class BaseSuite(object):
    '''
    BaseCase the base of cases
    '''
    def __init__(self):
        self.name = None


class HttpApiSuite(BaseSuite):
    def __init__(self):
        super().__init__()

    def constructor(self, ):
        pass

