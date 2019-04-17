# encoding='utf-8'
import functools
import inspect
import contextlib
import time
from haf.common.lock import Lock
from multiprocessing import Lock as m_lock


class TestDecorator:
    '''
    test decorate
    '''
    def __init__(self, name):
        self.name = name
        self.mark = "test"

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            if inspect.isfunction(args[0]):
                setattr(args[0], "test_decorator", self.__class__(self.name))
                setattr(args[0], "mark", self.mark)
                setattr(args[0], "run", True)
                return args[0]


test = TestDecorator


class SkipDecorator:
    '''
    test's skip
    '''
    def __init__(self, test_item: test=None):
        self.test_item = test_item
        self.test_item.run = False
        self.mark = "test"

    def __call__(self):
        setattr(self.test_item, "mark", self.mark)
        return self.test_item


skip = SkipDecorator


class ParameterizeDecorator:
    '''
    parameter decorate
    '''
    def __init__(self,  params: list=[]):
        self.params = params
        self.mark = "test"

    def __call__(self, *args, **kwargs):
        func = args[0]
        setattr(func, "mark", self.mark)
        setattr(func, "params", self.params)
        setattr(func, "run", True)
        return func


parameterize = ParameterizeDecorator


class Locker:
    '''
    locker
    '''
    def __init__(self, bus_client, key, lock: m_lock=None):
        self.bus_client = bus_client
        self.key = key
        self.local_lock = lock

    def get_lock(self):
        '''
        get lock from local_lock
        :return:
        '''
        if self.local_lock:
            self.local_lock.acquire()
            return

    def release_lock(self):
        '''
        release lock from local_lock
        :return:
        '''
        if self.local_lock:
            self.local_lock.release()
            return

# the lock decorator
def locker(func):
    @functools.wraps(func)
    def lock(self, *args, **kwargs):
        local_lock = None
        if len(args) > 0:
            key = args[0]
            if len(args) > 1:
                local_lock = args[1]
            else:
                local_lock = kwargs.get("lock", None)
        else:
            key = kwargs.get("key")
            local_lock = kwargs.get("lock", None)
        locker = Locker(self.bus_client, key, local_lock)
        locker.get_lock()
        result = func(self, *args, **kwargs)
        locker.release_lock()
        return result
    return lock


# the newlocker: can use with 'with'
@contextlib.contextmanager
def new_locker(bus_client, key, lock: m_lock=None):
    locker = Locker(bus_client, key, lock)
    locker.get_lock()
    try:
        yield
    finally:
        locker.release_lock()
        return