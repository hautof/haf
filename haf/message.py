#encoding='utf-8'

from multiprocessing.managers import BaseManager


class InfoManager(BaseManager): pass
'''
# InfoManager
#
'''


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

