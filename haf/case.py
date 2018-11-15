# encoding='utf-8'

from haf.config import  *
from haf.result import BaseResult, HttpApiResult


class BaseCase(object):
    '''
    BaseCase the base of cases
    '''
    def __init__(self):
        self.name = None
        self.id = None
        self.subid = None
        self.bentch = None
        self.type = None
        self.expect = None
        self.result = BaseResult()


class HttpApiCase(BaseCase):
    def __init__(self):
        super().__init__()
        self.type = CASE_TYPE_BASE
        self.message_type = MESSAGE_TYPE_CASE
        self.result = HttpApiResult()

    def _init_all(self):
        self.request = None
        self.response = None
        self.sql = None
        self.expect = None
