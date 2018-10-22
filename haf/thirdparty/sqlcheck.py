
from haf.pylib.Log.LogController import LogController
from haf.check.CheckSQLGet import CheckSQLGet
from haf.thirdparty.corpus_api.sqlcheck import sqlcheck as corpus_sqlcheck


logger = LogController.getLogger("corpus-checksql")


class sqlcheck(corpus_sqlcheck):
    '''
     SQL check third libs writen by third users
    '''
    def __init__(self):
        pass
    