# encoding='utf-8'


class BaseSuite(object):
    '''
    BaseSuite the base of suite
    '''
    def __init__(self):
        self.name = None


class HttpApiSuite(BaseSuite):
    '''
    http api suite
    '''
    def __init__(self):
        super().__init__()
        self.name = ""
        self.cases = []

    def constructor(self, name):
        self.name = name

    def add_case(self, case):
        self.cases.append(case)


class AppSuite(BaseSuite):
    '''
    app suite
    '''
    def __init__(self):
        super().__init__()
        self.name = ""
        self.cases = []

    def constructor(self, name):
        self.name = name

    def add_case(self, case):
        self.cases.append(case)



