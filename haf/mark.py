# encoding='utf-8'
import functools
import inspect
from haf.case import PyCase


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
