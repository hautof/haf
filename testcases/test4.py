#encoding='utf-8'

import sys

sys.path.append("..")
from haf.mark import test, skip, parameters
from haf.case import BaseCase
import inspect


class TestHello(BaseCase):

    @test("test hello11")
    def Hello(self):
        assert 1+1 == 2
        assert 1 == 5

    @skip
    @test("test hello12")
    def Hello1(self):
        assert 1 + 1 == 2

    @parameters([{"test":123},{"test":245}])
    def Hello2(self, params):
        print(params)
        assert 1 + 1 == 2


class TestHello2(BaseCase):
    @test("test hello2")
    def Hello(self):
        assert 1+1 == 2

    @test("test hello21")
    def Hello1123(self):
        assert 1 + 1 == 2



if __name__ == "__main__":
    th = TestHello()
    print(type(th))
    print(isinstance(th, BaseCase))
    print(issubclass(TestHello, BaseCase))
    print(isinstance(TestHello, BaseCase))
    print(dir(th))
    print(dir(BaseCase))
    print(dir(TestHello))
    print(isinstance(th.Hello, test))
    print(type(th.Hello))