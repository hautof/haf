# encoding='utf-8'

from haf.config import  *
from haf.result import BaseResult, HttpApiResult


class BaseSuite(object):
    '''
    BaseSuite the base of suite
    '''
    def __init__(self):
        self.name = None


class HttpApiSuite(BaseSuite):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.cases = []

    def constructor(self, name):
        self.name = name

    def add_case(self, case):
        self.cases.append(case)


