# encoding = 'utf-8'
import os
from haf.common.database import MysqlTool, SQLConfig
from haf.common.log import Log

logger = Log.getLogger(__name__)


class Publish(object):
    def __init__(self, sql_config: SQLConfig):
        self.sql_config = sql_config

    def load_sql_script(self):
        sql_script_path = "../resource/sqlpublish/haf_publish.sql"
        if os.path.exists(sql_script_path):
            with open(sql_script_path) as f:
                self.sql_script = "\n".join(f.readlines())
            return True
        else:
            logger.error(f"do not found sql file : {sql_script_path}")
            return False

    def check_db_exists(self):
        sql_check = ""


    def create_database(self):
        if not self.load_sql_script():
            return
        try:
            mysql_tool = MysqlTool()
            mysql_tool.connect_execute(self.sql_config, self.sql_script)
        except Exception as e:
            logger.error(e)

    def publish_result(self, results):
        if not results:
            logger.error("")
            return
        # TODO
        # publish to database 'haf_publish'
        
        

