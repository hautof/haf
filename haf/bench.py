# encoding='utf-8'
from haf.common.database import SQLConfig

from haf.case import HttpApiCase
from haf.config import  *


class BaseBench(object):
    '''
    BaseCase the base of cases
    '''
    def __init__(self):
        self.name = None
        pass


class HttpApiBench(BaseBench):
    def __init__(self):
        super().__init__()
        self.name = None
        self._init_all()

    def _init_all(self):
        self.cases = {}
        self.dbs = {}

    def add_case(self, case:HttpApiCase):
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def add_db(self, db:SQLConfig):
        key_db = str(db.id)
        self.dbs.update({key_db:db})

    def update_case(self, case: HttpApiCase):
        key = f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"
        self.cases.update({key: case})

    def get_case(self, key:str):
        return self.cases.get(key, None)

    def get_db(self, key:str):
        return self.dbs.get(key, None)