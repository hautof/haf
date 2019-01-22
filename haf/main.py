# encoding='utf-8'
import json
import os
import sys

from haf.program import Program
from haf.config import BANNER_STRS
import argparse


def init():
    print(BANNER_STRS)


def main_args():

    init()

    arg_program = argparse.ArgumentParser(prog="python -m haf", add_help=True)

    sub_all_arg_program = arg_program.add_subparsers(dest="all")

    sub_run_arg_program = sub_all_arg_program.add_parser("run",
                                                         help="run case, using `python -m haf run ` or `python -m haf` to run all case in local path ")
    sub_run_arg_program.add_argument("--case", "-case", dest="case", type=str,
                                     help="run cases wiht -case, path or file would be ok")
    sub_run_arg_program.add_argument("--runner-count", "-rc", dest="runner_count", type=int, default=1,
                                     help="runner count, default is 1 runner to run cases, max would be cpus*2")
    sub_run_arg_program.add_argument("--name", "-name", dest="name", type=str, default="AutoTest",
                                     help="test name, defautl is autotest")
    sub_run_arg_program.add_argument("--bus-server", "-bs", dest="bus_server", type=str, default=None,
                                     help="""default is localhost to run bus server;
                                             if is ip or domain, would not run local bus-server, and using ip to connect""")
    sub_run_arg_program.add_argument("--web-server", "-ws", type=bool,
                                     help="""default is not run;
                                             if is True, would create web server to offer the api and html service;""")
    sub_run_arg_program.add_argument("--report-html", "-rh", type=bool, default=True,
                                     help="""default is True,to generate html report""")
    sub_run_arg_program.add_argument("--report-output-dir", "-rod", dest="report_output_dir", type=str, default="",
                                     help="""default is "", using to generate report to this path""")
    sub_run_arg_program.add_argument("--report-template", "-rt", type=str, default="base", dest="report_template",
                                     help="""default using base to generate report;
                                            customer template is support too""")
    sub_run_arg_program.add_argument("--log-dir", "-ld", type=str, dest="log_dir",
                                     help="""log output dir is needed!""")
    sub_run_arg_program.add_argument("--only-loader", "-ol", type=bool, default=False, dest="only_loader",
                                     help="""if true, only start loader""")
    sub_run_arg_program.add_argument("--only-bus", "-ob", type=bool, default=False, dest="only_bus",
                                     help="""if true, only start bus""")
    sub_run_arg_program.add_argument("--only-runner", "-or", type=bool, default=False, dest="only_runner",
                                     help="""if true, only start runner""")
    sub_run_arg_program.add_argument("--only-recorder", "-ore", type=bool, default=False, dest="only_recorder",
                                     help="""if true, only start recorder""")
    sub_run_arg_program.add_argument("--config", "-c", type=str, dest="config",
                                     help="""customer config""")
    sub_run_arg_program.add_argument("--api", "-api", dest="api", default=True, type=bool,
                                     help="api case or not, default is true")
    sub_run_arg_program.add_argument("--debug", "-debug", dest="debug", default=False, type=bool,
                                     help="open debug or not")
    sub_run_arg_program.add_argument("--sql-publish", "-sp", dest="sql_publish", default=False, type=bool,
                                     help="sql publish or not")
    sub_run_arg_program.add_argument("--sql-publish-db", "-sp_db", dest="sql_publish_db", type=str, default="",
                                     help="sql publish db config, format like : host:port@username:password@database)")

    args = arg_program.parse_args()
    main_program = Program()

    if args.all == "run":
        # here : config <- file
        if args.config:
            if not os.path.exists(args.config):
                print(f"config file {args.config} not found!")
                sys.exit(-1)
            try:
                with open(args.config, 'r') as f:
                    config = json.load(f).get("config")
                    config_run = config.get("run")
                    args.name = config.get("name")
                    args.log_dir = config_run.get("log").get("log_path")
                    bus_config = config_run.get("bus")
                    args.only_bus = bus_config.get("only")
                    args.bus_server = None if bus_config.get("host") is None or bus_config.get("host")=="" else f"{bus_config.get('auth_key')}@{bus_config.get('host')}:{bus_config.get('host')}"
                    args.report_output_dir = config_run.get("report").get("report_path")
                    args.report_template = config_run.get("report").get("report_template", "None")
                    args.case = [ x.get("case_path") for x in config_run.get("case") ]
                    runner_config = config_run.get("runner")
                    args.runner_count = runner_config.get("count")
                    args.only_runner = runner_config.get("only")
                    args.web_server = config_run.get("web_server").get("run")
                    publish_sql = config_run.get("sql_publish", None)
                    if publish_sql and publish_sql.get("publish"):
                        args.sql_publish = publish_sql.get("publish")
                        from haf.common.database import SQLConfig
                        sql_config = SQLConfig()
                        sql_config.constructor(publish_sql)
                        args.sql_publish_db = sql_config
                    else:
                        args.sql_publish = False
            except Exception as e:
                print(e)
                sys.exit(-1)

        if isinstance(args.case, str):
            if not isinstance(args.case, list):
                args.case = [str(case) for case in args.case.split(",")]
        if args.runner_count:
            pass

        if args.sql_publish:
            if isinstance(args.sql_publish_db, str):
                from haf.common.database import SQLConfig
                sql_config = SQLConfig()
                hp, up, db = args.sql_publish_db.split('@')
                host, port = hp.split(':')
                username, password = up.split(':')
                sc_dict = {
                    "host": host, "port": port, "username": username, "password": password, "id":0, "sql_name": "haf-publish", "protocol": "mysql"
                }
                sql_config.constructor(sc_dict)
                args.sql_publish_db = sql_config

        # here : bus server <- password@host:port
        if args.bus_server:
            if "@" in args.bus_server and ":" in args.bus_server:
                password, temp = args.bus_server.split("@")
                host, port = temp.split(":")
                args.bus_server = [bytes(password, encoding='utf-8'), host, int(port)]
        if args.web_server:
            pass

        # here : case <- dir/file
        cases = []
        for case in args.case:
            cases.append(case)
        args.case = []
        for path in cases:
            if not path.endswith(".py") and not path.endswith(".yml") and not path.endswith(".json") and not path.endswith(".xlsx"):
                if os.path.exists(path) and os.path.isdir(path):
                    file_list = os.listdir(path)
                    for f in file_list:
                        if f.startswith("test_") and (f.endswith(".py") or f.endswith(".yml") or f.endswith(".json") or f.endswith(".xlsx")):
                            args.case.append(os.path.join(path, f))
                else:
                    print("found wrong case path ...")
            else:
                args.case.append(path)

        print(args)
        main_program.run(args)
    else:
        print("using python -m haf help to show help infos")


