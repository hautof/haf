# encoding='utf-8'
import functools
import inspect
import time

from haf.case import PyCase
from haf.common.lock import Lock


class TestDecorator:
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
    def __init__(self, test_item: test=None):
        self.test_item = test_item
        self.test_item.run = False
        self.mark = "test"

    def __call__(self):
        setattr(self.test_item, "mark", self.mark)
        return self.test_item


skip = SkipDecorator


class ParameterizeDecorator:
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
    def __init__(self, bus_client, key):
        self.bus_client = bus_client
        self.key = key

    def get_lock(self):
        if self.key == "result":
            lock = self.bus_client.get_lock()
        elif self.key == "web":
            lock = self.bus_client.get_web_lock()
        elif self.key == "case":
            lock = self.bus_client.get_case_lock()
        while True:
            if not lock.empty():
                return lock.get()
            time.sleep(0.1)

    def release_lock(self):
        if self.key == "result":
            return self.bus_client.get_lock().put(Lock)
        elif self.key == "web":
            return self.bus_client.get_web_lock().put(Lock)
        elif self.key == "case":
            return self.bus_client.get_case_lock().put(Lock)


def locker(func):
    @functools.wraps(func)
    def lock(self, *args, **kwargs):
        if len(args) > 0:
            key = args[0]
        else:
            key = kwargs.get("key")
        locker = Locker(self.bus_client, key)
        locker.get_lock()
        func(self, *args, **kwargs)
        locker.release_lock()
        return
    return lock