# -*- coding: utf-8 -*-

def _init():
    global _global_dict
    _global_dict = {}
    _global_dict["TestSuiteList"] = []
    global TestSuiteList
    TestSuiteList = []

def append(value):
    TestSuiteList.append(value)

def getTestSuiteList():
    return TestSuiteList

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue