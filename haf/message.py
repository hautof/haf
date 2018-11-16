#encoding='utf-8'

from haf.case import HttpApiCase
from haf.result import HttpApiResult


class MessageDict(object):
    '''
    # DictItem
    # replace the default dict
    '''
    def __init__(self):
        self.items = dict()

    def set(self, key, value):
        self.items[key] = value

    def get(self, key):
        self.items.get(key, None)

    def __setitem__(self, key, value):
        self.set(key, value)


class MessageGenerator(object):

    @staticmethod
    def generate(input):
        if isinstance(input, HttpApiCase):
            MessageGenerator.generate_httpapicase(input)
        elif isinstance(input, HttpApiResult):
            MessageGenerator.generate_httpapiresult(input)

    @staticmethod
    def generate_httpapicase(input):
        pass