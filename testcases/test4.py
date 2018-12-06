#encoding='utf-8'

import sys

sys.path.append("..")
from haf.mark import test, skip, parameterize
from haf.case import BaseCase


class TestHello(BaseCase):

    @test("test hello11")
    def test_1(self):
        assert 1+1 == 2
        assert 1 == 5

    @skip
    @test("test hello12")
    def test_2(self):
        assert 1 + 1 == 2

    @test
    @parameterize([{"test":123},{"test":245}])
    def test_3(self, params):
        print(params)
        assert 1 + 1 == 2

    @parameterize([{"test":123},{"test":245}])
    def test_4(self, params):
        assert params.get("test")==123


class TestHello2(BaseCase):
    @test("test hello2")
    def test1(self):
        assert 1+1 == 2

    @test("test hello21")
    def test2(self):
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