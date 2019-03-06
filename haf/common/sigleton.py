# encoding='utf-8'


class SingletonType(type):

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super(SingletonType, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(SingletonType, self).__call__(*args, **kwargs)
        return self.__instance