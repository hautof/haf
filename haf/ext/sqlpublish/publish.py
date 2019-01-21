# encoding = 'utf-8'
import os

from haf.apihelper import Ids, Response, Request
from haf.case import HttpApiCase
from haf.common.database import MysqlTool, SQLConfig
from haf.common.log import Log
from haf.result import EndResult, Summary, Detail
from haf.ext.sqlpublish.createhaf import *
logger = Log.getLogger(__name__)


class DBMain(object):
    def __init__(self, id, name, begin_time, end_time, duration_time, passed, failed, skip, error, suite_name):
        self.id = id
        self.name = name
        self.begin_time = begin_time
        self.end_time = end_time
        self.duration_time = duration_time
        self.passed = passed
        self.failed = failed
        self.skip = skip
        self.error = error
        self.suite_name = suite_name
    

class DBSuite(object):
    def __init__(self, id, main_id, suite_name):
        self.id = id
        self.main_id = main_id
        self.suite_name = suite_name


class DBSummary(object):
    def __init__(self, id, name, passed, failed, skip, error, all, base_url, begin_time, end_time, duration_time, suite_id):
        self.id = id
        self.name = name
        self.passed = passed
        self.failed = failed
        self.skip = skip
        self.error = error
        self.all = all
        self.base_url = base_url
        self.begin_time = begin_time
        self.end_time = end_time
        self.duration_time = duration_time
        self.suite_id = suite_id


class DBDetail(object):
    def __init__(self, id, case_name, result_check_response, result_check_sql_response, run_error, result, begin_time, end_time, log_dir, runner):
        self.id = id
        self.case_name = case_name
        self.result_check_response = result_check_response
        self.result_check_sql_response = result_check_sql_response
        self.run_error = run_error
        self.result = result
        self.begin_time = begin_time
        self.end_time = end_time
        self.log_dir = log_dir
        self.runner = runner


class DBCase(object):
    def __init__(self, id, ids_id, run, dependent, bench_name, request_id, response_id, expect_id, sqlinfo_id, type, detail_id, suite_id):
        self.id = id
        self.ids_id = ids_id
        self.run = run
        self.dependent = dependent
        self.bench_name = bench_name
        self.request_id = request_id
        self.response_id = response_id
        self.expect_id = expect_id
        self.sqlinfo_id = sqlinfo_id
        self.type = type
        self.detail_id = detail_id
        self.suite_id = suite_id

class DBCaseExpect(object):
    def __init__(self, id, response_id, sql_check_func, sql_response_reust):
        self.id = id
        self.response_id = response_id
        self.sql_check_func = sql_check_func
        self.sql_response_result = sql_response_reust


class DBCaseIds(object):
    def __init__(self, id, case_id, case_sub_id, case_name, case_api_name):
        self.id = id
        self.case_id = case_id
        self.case_sub_id = case_sub_id
        self.case_name = case_name
        self.case_api_name = case_api_name


class DBCaseRequest(object):
    def __init__(self, id, header, data, url, method, protocol, host_port):
        self.id = id
        self.header = header
        self.data = data
        self.url = url
        self.method = method
        self.protocol = protocol
        self.host_port = host_port


class DBCaseResponse(object):
    def __init__(self, id, header, body, code):
        self.id = id
        self.header = header
        self.body = body
        self.code = code


class DBCaseSqlinfo(object):
    def __init__(self, id, scripts_id, config_id, check_list_id):
        self.id = id
        self.scripts_id = scripts_id
        self.config_id = config_id
        self.check_list_id = check_list_id


class DBCaseSqlinfoChecklist(object):
    def __init__(self, id, sql_response):
        self.id = id
        self.sql_response = sql_response


class DBCaseSqlinfoScript(object):
    def __init__(self, id, sql_response):
        self.id = id
        self.sql_response = sql_response


class DBCaseSqlinfoConfig(object):
    def __init__(self, id, host, port, type, username, password):
        self.id = id
        self.host = host
        self.port = port
        self.type = type
        self.username = username
        self.password = password



class SQLPublish(object):
    def __init__(self):
        pass
    
    def insert_main(self, db_main: DBMain):
        sql_sc = f"""insert into main (name, begin_time, end_time, duration_time, passed, failed, skip, error, suite_name) 
                    values ({db_main.name}, {db_main.begin_time}, {db_main.end_time}, {db_main.duration_time}, {db_main.passed}, 
                            {db_main.failed}, {db_main.skip}, {db_main.error}, {db_main.suite_name}); SELECT @@IDENTITY AS Id """

    def insert_suite(self, db_suite: DBSuite):
        sql_sc = f"""insert into suite (main_id, suite_name)
                    values ({db_suite.main_id}, {db_suite.suite_name}); SELECT @@IDENTITY AS Id """

    def insert_detail(self, db_detail: DBDetail):
        sql_sc = f"""insert into detail (suite_id, case_name, result_check_response, resulte_check_sql_response, run_error, result, begin_time, end_time, case_id, log_dir, runner)
                    values ({db_detail.suite_id}, {db_detail.case_name}, {db_detail.result_check_response}, {db_detail.result_check_response},
                            {db_detail.run_error}, {db_detail.result}, {db_detail.begin_time}, {db_detail.end_time}, {db_detail.case_id}, {db_detail.log_dir}, {db_detail.runner}); SELECT @@IDENTITY AS Id """

    def insert_summary(self, db_summary: DBSummary):
        sql_sc = f"""insert into summary (name, passed, failed, skip, error, all, base_url, begin_time, end_time, duration_time, suite_id)
                    values ({db_summary.name}, {db_summary.passed}, {db_summary.failed}, {db_summary.skip},
                            {db_summary.error}, {db_summary.all}, {db_summary.base_url}, {db_summary.begin_time}, {db_summary.end_time},
                            {db_summary.duration_time, db_summary.suite_id}); SELECT @@IDENTITY AS Id """

    def insert_case(self, db_case: DBCase):
        sql_sc = f"""insert into case (ids_id, run, dependent, bench_name, request_id, response_id, expect_id, sqlinfo_id, type, suite_id) 
                    values ({db_case.ids_id}, {db_case.run}, {db_case.dependent}, {db_case.bench_name}, {db_case.request_id}, {db_case.response_id},
                            {db_case.expect_id}, {db_case.sqlinfo_id}, {db_case.type}, {db_case.suite_id}); SELECT @@IDENTITY AS Id """

    def insert_caseexpect(self, db_case_expect: DBCaseExpect):
        sql_sc = f"""insert into case_expect (response_id, sql_check_func, sql_response_result)
                    values ({db_case_expect.response_id, db_case_expect.sql_check_func, db_case_expect.sql_response_result}); SELECT @@IDENTITY AS Id """

    def insert_case_ids(self, db_caseid: DBCaseIds):
        sql_sc = f"""insert into case_ids (case_id, case_sub_id, case_name, case_api_name) 
                    values ({db_caseid.case_id}, {db_caseid.case_name}, {db_caseid.case_api_name}); SELECT @@IDENTITY AS Id """

    def insert_case_request(self, db_caserequest: DBCaseRequest):
        sql_sc = f"""insert into case_request (header, data, url, method, protocol, host_port) 
                    values ({db_caserequest.header}, {db_caserequest.data}, {db_caserequest.url}, {db_caserequest.method}, {db_caserequest.protocol}, {db_caserequest.host_port}); SELECT @@IDENTITY AS Id """

    def insert_case_response(self, db_caseresponse: DBCaseResponse):
        sql_sc = f"""insert into case_response (header, body, code) 
                    values ({db_caseresponse.header}, {db_caseresponse.body}, {db_caseresponse.code}); SELECT @@IDENTITY AS Id """

    def insert_case_sqlinfo(self, db_casesqlinfo: DBCaseSqlinfo):
        sql_sc = f"""insert into case_sqlinfo (scripts_id, config_id, check_list_id)
                    values ({db_casesqlinfo.scripts_id}, {db_casesqlinfo.config_id}, {db_casesqlinfo.check_list_id}); SELECT @@IDENTITY AS Id """

    def insert_case_sqlinfochecklist(self, db_casesqlinfo_checklist: DBCaseSqlinfoChecklist):
        sql_sc = f"""insert into case_sqlinfo_checklist (sql_response) values ({db_casesqlinfo_checklist.sql_response}); SELECT @@IDENTITY AS Id """

    def insert_case_sqlinfoscript(self, db_casesqlinfo_script: DBCaseSqlinfoScript):
        sql_sc = f"""insert into case_sqlinfo_script (sql_response) values ({db_casesqlinfo_script.sql_response}); SELECT @@IDENTITY AS Id """

    def insert_case_sqlinfoconfig(self, db_casesqlinfo_config: DBCaseSqlinfoConfig):
        sql_sc = f"""insert into case_sqlinfo_config (host, port, type, username, password)
                    values ({db_casesqlinfo_config.host}, {db_casesqlinfo_config.port}, {db_casesqlinfo_config.type}, {db_casesqlinfo_config.username}, {db_casesqlinfo_config.password}"""


class Publish(object):
    def __init__(self, sql_config: SQLConfig):
        self.sql_config = sql_config

        self.mysql_tool = MysqlTool()

    # no use here from now
#
#     def load_sql_script(self):
#         local_dir = os.path.dirname(__file__)
#         sql_script_path = f"{local_dir}/../resource/sqlpublish/haf_publish.sql"
#         logger.info(f"load sql script file : {sql_script_path}")
#         if os.path.exists(sql_script_path):
#             with open(sql_script_path) as f:
#                 self.sql_script = f.read().replace("\n", "")
#             return True
#         else:
#             logger.error(f"do not found sql file : {sql_script_path}")
#             return False
#

    def check_db_exists(self):
        try:
            sql_check = "show databases"
            result = self.mysql_tool.connect_execute(self.sql_config, sql_check)
            if len(result) > 0 and len(result[0]) > 0:
                for x in result[0]:
                    if "haf_publish" in x:
                        return True
            return False
        except Exception as e:
            logger.error(e)

    def create_database(self):
        try:
            if not self.check_db_exists():
                for case in create_case:
                    self.mysql_tool.connect_execute(self.sql_config, case)
        except Exception as e:
            logger.error(e)

    def publish_result(self, results: EndResult):

        if not results:
            logger.error("no result need publish")
            return
        self.create_database()
        try:
            sql_publish = SQLPublish()
            db_main = DBMain(0, results.name, results.begin_time, results.end_time, results.duration, results.passed, results.failed, results.skip, results.error, results.suite_name)
            main_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_main(db_main))[0][0]
            for suite_name in results.suite_name:

                db_suite = DBSuite(0, main_id, suite_name)
                suite_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_suite(db_suite))[0][0]

                s = results.summary.get(suite_name)
                s = Summary()
                db_summary = DBSummary(0, suite_name, s.passed, s.failed, s.skip, s.error, s.all, s.base_url, s.begin_time, s.end_time, s.duration, suite_id)
                self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_summary(db_summary))

                d = results.details.get(suite_name)
                d = Detail()
                for case in d.cases:
                    case = HttpApiCase()
                    ids = case.ids
                    db_case_ids = DBCaseIds(0, ids.id, ids.subid, ids.name, ids.api_name)
                    case_ids_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case_ids(db_case_ids))[0][0]

                    response = case.response
                    db_case_response = DBCaseResponse(0, response.header, response.body, response.code)
                    case_response_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case_response(db_case_response))[0][0]

                    request = case.request
                    db_case_request = DBCaseRequest(0, request.header, request.data, request.url, request.method, request.protocol, request.host_port)
                    case_request_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case_request(db_case_request))[0][0]

                    expect = case.expect
                    db_case_expect = DBCaseExpect(0, expect.response, expect.sql_check_func, expect.sql_response_result)
                    case_expect_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_caseexpect(db_case_expect))[0][0]

                    sqlinfo_script = case.sqlinfo.scripts
                    db_case_script = DBCaseSqlinfoScript(0, sqlinfo_script["sql_response"])
                    sqlinfo_script_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case_sqlinfoscript(db_case_script))[0][0]

                    sqlinfo_checklist = case.sqlinfo.check_list
                    db_case_checklist = DBCaseSqlinfoChecklist(0, sqlinfo_checklist["sql_response"])
                    sqlinfo_checklist_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case_sqlinfochecklist(db_case_checklist))[0][0]

                    sqlinfo_config = case.sqlinfo.config
                    db_case_sqlinfoconfig = DBCaseSqlinfoConfig(0, sqlinfo_config.host, sqlinfo_config.port, sqlinfo_config.type, sqlinfo_config.username, sqlinfo_config.password)
                    sqlinfo_config_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case_sqlinfoconfig(db_case_sqlinfoconfig))[0][0]

                    case_sqlinfo = DBCaseSqlinfo(0, sqlinfo_script_id, sqlinfo_config_id, sqlinfo_checklist_id)
                    case_sqlinfo_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case_sqlinfo(case_sqlinfo))[0][0]

                    case_detail = DBDetail(0, case.name, case.result_check_response, case.result_check_sql_response, case.run_error, case.result, case.begin_time, case.end_time, case.log_dir, case.runner)
                    case_detail_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_detail(case_detail))[0][0]

                    db_case = DBCase(0, case_ids_id, case.run, case.dependent, case.bench_name, case_request_id, case_response_id, case_expect_id, case_sqlinfo_id, case.type, case_detail_id, suite_id)
                    self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_case(db_case))

        except Exception as e:
            logger.error(e)
        
        

