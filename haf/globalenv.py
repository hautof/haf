# -*- coding: utf-8 -*-
'''
file name : globalenv
desc : using to multi file var shared
'''

def _init():
    '''
    global init
    :return:
    '''
    global _global_dict
    _global_dict = {}


def set_global(name, value):
    '''
    set global var
    :param name:
    :param value:
    :return:
    '''
    _global_dict[name] = value


def get_global(name, defValue=None):
    '''
    get from global
    :param name:
    :param defValue:
    :return:
    '''
    try:
        return _global_dict[name]
    except KeyError:
        return defValue