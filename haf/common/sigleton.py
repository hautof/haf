# encoding='utf-8'
'''
file name : sigleton
description : the sigleton defined
others:
    usage:
    1, class A(metaclass=SingletonType):
    2, class B(Singleton)
    3, @sigleton
       class C(object):

'''


# this is metaclass
class SingletonType(type):

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super(SingletonType, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(SingletonType, self).__call__(*args, **kwargs)
        return self.__instance


# this is decorator
def singleton(cls):
    __instance = {}
    def _wraps(*args, **kwargs):
        if cls not in __instance:
            __instance[cls] == cls(*args, **kwargs)
        return __instance[cls]
    return _wraps


# this is class
class Singleton(object):
    import threading
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with Singleton._lock:
                if not hasattr(cls, "_instance"):
                    Singleton._instance = super().__new__(cls)
        return Singleton._instance


