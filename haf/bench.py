# encoding='utf-8'
'''
file name : bench
description : the test bench
others:
    include All Case bench
'''
from haf.common.database import SQLConfig
from haf.case import HttpApiCase, AppCase, WebCase


class BaseBench(object):
    '''
    BaseCase the base of cases
    '''
    def __init__(self, args):
        self.name = None
        self.args = args
        pass


class PyBench(BaseBench):
    '''
    py case bench
    '''
    def __init__(self, args):
        self.name = None
        self.args = args
        super().__init__(args)
        self._init_all()

    def _init_all(self):
        '''
        init all bench
        :return:
        '''
        self.cases = {}
        self.dbs = {}

    def add_case(self, case):
        '''
        add case to bench
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def add_db(self, db: SQLConfig):
        '''
        add database config to bench
        :param db:
        :return:
        '''
        key_db = str(db.id)
        self.dbs.update({key_db: db})

    def update_case(self, case):
        '''
        update case of the exists case
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def get_case(self, key: str) -> 'Case':
        '''
        get case by key
        :param key:
        :return: case
        '''
        return self.cases.get(key, None)

    def get_db(self, key: str) -> 'SQLConfig':
        '''
        get db by key
        :param key:
        :return: database config
        '''
        return self.dbs.get(key, None)


class HttpApiBench(BaseBench):
    '''
    the api bench
    '''
    def __init__(self, args):
        self.name = None
        self.args = args
        super().__init__(args)
        self._init_all()

    def _init_all(self):
        '''
        init bench
        :return:
        '''
        self.cases = {}
        self.dbs = {}

    def add_case(self, case:HttpApiCase):
        '''
        add case to bench
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def add_db(self, db:SQLConfig):
        '''
        add db to bench
        :param db:
        :return:
        '''
        key_db = str(db.id)
        self.dbs.update({key_db:db})

    def update_case(self, case: HttpApiCase):
        '''
        update exists case
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def get_case(self, key:str) -> 'Case':
        '''
        get case by key
        :param key:
        :return: case
        '''
        return self.cases.get(key, None)

    def get_db(self, key:str) -> 'SQLConfig':
        '''
        get database config by key
        :param key:
        :return: sqlconfig
        '''
        return self.dbs.get(key, None)


class AppBench(BaseBench):
    '''
    app bench
    '''
    def __init__(self, args):
        self.name = None
        self.args = args
        super().__init__(args)
        self._init_all()

    def _init_all(self):
        '''
        init bench
        :return:
        '''
        self.cases = {}
        self.dbs = {}

    def add_case(self, case: AppCase):
        '''
        add case to bench
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def add_db(self, db: SQLConfig):
        '''
        add db to bench
        :param db:
        :return:
        '''
        key_db = str(db.id)
        self.dbs.update({key_db:db})

    def update_case(self, case: AppCase):
        '''
        update exists case
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def get_case(self, key:str) -> 'Case':
        '''
        get case by key
        :param key:
        :return: case
        '''
        return self.cases.get(key, None)

    def get_db(self, key:str) -> 'SQLConfig':
        '''
        get database config by key
        :param key:
        :return: sqlconfig
        '''
        return self.dbs.get(key, None)


class WebBench(BaseBench):
    '''
    web bench
    '''
    def __init__(self, args):
        self.name = None
        self.args = args
        super().__init__(args)
        self._init_all()

    def _init_all(self):
        '''
        init bench
        :return:
        '''
        self.cases = {}
        self.dbs = {}

    def add_case(self, case: AppCase):
        '''
        add case to bench
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def add_db(self, db: SQLConfig):
        '''
        add db to bench
        :param db:
        :return:
        '''
        key_db = str(db.id)
        self.dbs.update({key_db:db})

    def update_case(self, case: AppCase):
        '''
        update exists case
        :param case:
        :return:
        '''
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def get_case(self, key:str) -> 'Case':
        '''
        get case by key
        :param key:
        :return: case
        '''
        return self.cases.get(key, None)

    def get_db(self, key:str) -> 'SQLConfig':
        '''
        get database config by key
        :param key:
        :return: sqlconfig
        '''
        return self.dbs.get(key, None)