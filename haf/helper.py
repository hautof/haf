# encoding='utf-8'
'''
file name : helper
desc : show help informations
'''

import os, sys
from haf.config import *


class Helper(object):
    def __init__(self):
        pass
        # include init_workspace

    def init_workspace(self, case_type: str=None):
        ''' init haf workspace with type case'''
        if case_type:
            pass
        else:
            self.get_files_from_github()

    def get_files_from_github(self):
        os.system("git clone https://github.com/tsbxmw/haf-sample")

    @staticmethod
    def print_help():
        '''
        show help informations
        '''
        run_help = """
        [1] usage: python -m haf init [--type TYPE]
        
        optional arguments:
        default : init the workspace with haf-samples

        [2] usage: python -m haf run [-h] [--name NAME] [--case CASE] [--api API]
                         [--only-runner ONLY_RUNNER]
                         [--runner-count RUNNER_COUNT]
                         [--bus-server BUS_SERVER]
                         [--bus-server-port BUS_SERVER_PORT]
                         [--only-bus ONLY_BUS] [--web-server WEB_SERVER]
                         [--report-html REPORT_HTML]
                         [--report-output-dir REPORT_OUTPUT_DIR]
                         [--report-template REPORT_TEMPLATE]
                         [--report-export-template REPORT_EXPORT_TEMPLATE]
                         [--report-export-dir REPORT_EXPORT_DIR]
                         [--log-dir LOG_DIR] [--only-loader ONLY_LOADER]
                         [--only-recorder ONLY_RECORDER] [--config CONFIG]
                         [--debug DEBUG] [--sql-publish SQL_PUBLISH]
                         [--sql-publish-db SQL_PUBLISH_DB]

        optional arguments:
        -h, --help            show this help message and exit
        --name NAME, -name NAME
                                test name, defautl is autotest
        --case CASE, -case CASE
                                run cases wiht -case, path or file would be ok
        --api API, -api API   api case or not, default is true
        --only-runner ONLY_RUNNER, -or ONLY_RUNNER
                                if true, only start runner
        --runner-count RUNNER_COUNT, -rc RUNNER_COUNT
                                runner count, default is 1 runner to run cases, max
                                would be cpus*2
        --bus-server BUS_SERVER, -bs BUS_SERVER
                                default is localhost to run bus server; if is ip or
                                domain, would not run local bus-server, and using ip
                                to connect
        --bus-server-port BUS_SERVER_PORT, -bsp BUS_SERVER_PORT
                                default is 9000, using another port to start bus
                                server
        --only-bus ONLY_BUS, -ob ONLY_BUS
                                if true, only start bus
        --web-server WEB_SERVER, -ws WEB_SERVER
                                default is not run; if is True, would create web
                                server to offer the api and html service;
        --report-html REPORT_HTML, -rh REPORT_HTML
                                default is True,to generate html report
        --report-output-dir REPORT_OUTPUT_DIR, -rod REPORT_OUTPUT_DIR
                                default is "", using to generate report to this path
        --report-template REPORT_TEMPLATE, -rt REPORT_TEMPLATE
                                default using base to generate report; customer
                                template is support too
        --report-export-template REPORT_EXPORT_TEMPLATE, -ret REPORT_EXPORT_TEMPLATE
                                email report template
        --report-export-dir REPORT_EXPORT_DIR, -red REPORT_EXPORT_DIR
                                email report dir
        --log-dir LOG_DIR, -ld LOG_DIR
                                log output dir is needed!
        --only-loader ONLY_LOADER, -ol ONLY_LOADER
                                if true, only start loader
        --only-recorder ONLY_RECORDER, -ore ONLY_RECORDER
                                if true, only start recorder
        --config CONFIG, -c CONFIG
                                customer config
        --debug DEBUG, -debug DEBUG
                                open debug or not
        --sql-publish SQL_PUBLISH, -sp SQL_PUBLISH
                                sql publish or not
        --sql-publish-db SQL_PUBLISH_DB, -sp_db SQL_PUBLISH_DB
                                sql publish db config, format like :
                                host:port@username:password@database)
        --no-output NO_OUTPUT, -nout NOUT
                                no output
        --local-logger LOCAL_LOGGER, -llog LLOG
                                local logger writer
        ---filter TEST_FILTER, -t
        """

        print(run_help)
