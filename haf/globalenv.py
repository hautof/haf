# -*- coding: utf-8 -*-
from haf.message import MessageDict


def _init():
    global _global_dict
    _global_dict = MessageDict()

def set_global(name, value):
    _global_dict[name] = value

def get_global(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue