# encoding='utf-8'
import json
import os
import sys

from haf.pluginmanager import PluginManager, plugin_manager
from haf.program import Program
from haf.helper import Helper
from haf.config import BANNER_STRS
from haf.common.schema import check_config
import argparse


def init():
    print(BANNER_STRS)


def main_args():

    init()

    arg_program = argparse.ArgumentParser(prog="python -m haf", add_help=True)

    sub_all_arg_program = arg_program.add_subparsers(dest="all")

    sub_run_arg_program = sub_all_arg_program.add_parser("run",
                                                         help="run case, using `python -m haf run ` or `python -m haf` to run all case in local path ")
    # name
    sub_run_arg_program.add_argument("--name", "-name", dest="name", type=str, default="AutoTest",
                                     help="test name, defautl is autotest")
    # case
    sub_run_arg_program.add_argument("--case", "-case", dest="case", type=str,
                                     help="run cases wiht -case, path or file would be ok")
    sub_run_arg_program.add_argument("--api", "-api", dest="api", default=True, type=bool,
                                     help="api case or not, default is true")
    # runner
    sub_run_arg_program.add_argument("--only-runner", "-or", type=bool, default=False, dest="only_runner",
                                     help="""if true, only start runner""")
    sub_run_arg_program.add_argument("--runner-count", "-rc", dest="runner_count", type=int, default=1,
                                     help="runner count, default is 1 runner to run cases, max would be cpus*2")
    # bus server
    sub_run_arg_program.add_argument("--bus-server", "-bs", dest="bus_server", type=str, default=None,
                                     help="""default is localhost to run bus server;
                                             if is ip or domain, would not run local bus-server, and using ip to connect""")
    sub_run_arg_program.add_argument("--bus-server-port", "-bsp", dest="bus_server_port", type=int,
                                     help="""default is 9000, using another port to start bus server""")
    sub_run_arg_program.add_argument("--only-bus", "-ob", type=bool, default=False, dest="only_bus",
                                     help="""if true, only start bus""")
    # report
    sub_run_arg_program.add_argument("--report-html", "-rh", type=bool, default=True,
                                     help="""default is True,to generate html report""")
    sub_run_arg_program.add_argument("--report-output-dir", "-rod", dest="report_output_dir", type=str, default="",
                                     help="""default is "", using to generate report to this path""")
    sub_run_arg_program.add_argument("--report-template", "-rt", type=str, default="base", dest="report_template",
                                     help="""default using base to generate report;
                                            customer template is support too""")
    sub_run_arg_program.add_argument("--report-export-template", "-ret", type=str, dest="report_export_template",
                                     help="""email report template""")
    sub_run_arg_program.add_argument("--report-export-dir", "-red", type=str, dest="report_export_dir",
                                     help="""email report dir""")
    # log
    sub_run_arg_program.add_argument("--log-dir", "-ld", type=str, dest="log_dir",
                                     help="""log output dir is needed!""")
    # loader
    sub_run_arg_program.add_argument("--only-loader", "-ol", type=bool, default=False, dest="only_loader",
                                     help="""if true, only start loader""")
    # recorder
    sub_run_arg_program.add_argument("--only-recorder", "-ore", type=bool, default=False, dest="only_recorder",
                                     help="""if true, only start recorder""")
    # config
    sub_run_arg_program.add_argument("--config", "-c", type=str, dest="config",
                                     help="""customer config""")
    # debug
    sub_run_arg_program.add_argument("--debug", "-debug", dest="debug", default=False, type=bool,
                                     help="open debug or not")
    # console
    sub_run_arg_program.add_argument("--console", "-cmd", dest="console", default=False, type=bool,
                                     help="open console or not")
    # no output
    sub_run_arg_program.add_argument("--no-output", "-nout", dest="nout", default=False, type=bool,
                                     help="do not show output")
    # case filter
    sub_run_arg_program.add_argument("--filter-case", "-fc", dest="filter_case", default=None, type=str,
                                     help="only run filter cases's include cases, filter by name")
    # local logger
    sub_run_arg_program.add_argument("--local-logger", "-llog", dest="local_logger", default=None, type=str,
                                     help="local logger to make runner faster than now!")

    # init
    sub_init_arg_program = sub_all_arg_program.add_parser("init",
                                                         help="init workspace, using 'python -m haf init -t=all' to init workspace of haf")
    sub_init_arg_program.add_argument("--type", "-t", dest="init_type", type=str, default=None,
                                     help="init workspace with type")
    # help
    sub_help_arg_program = sub_all_arg_program.add_parser("help",
                                                         help="help, using 'python -m haf help' to show this")
    sub_help_arg_program.add_argument("--all", dest="help-all", type=str, default=None,
                                     help="show all help informations")

    plugin_manager.add_options(sub_run_arg_program)

    args = arg_program.parse_args()

    if args.all == "run":
        # here : config <- file
        if args.config:
            if not os.path.exists(args.config):
                print(f"config file <{args.config}> not found!")
                sys.exit(-1)
            try:
                with open(args.config, 'r') as f:
                    all_config_json  = json.load(f)
                    if not check_config(all_config_json):
                        sys.exit(-1)
                    config = all_config_json.get("config")
                    config_run = config.get("run")
                    args.name = config.get("name")
                    args.log_dir = config_run.get("log").get("log_path")
                    bus_config = config_run.get("bus")
                    args.bus_server_port = config_run.get("bus_server_port")
                    args.only_bus = bus_config.get("only")
                    args.bus_server = None if bus_config.get("host") is None or bus_config.get("host")=="" else f"{bus_config.get('auth_key')}@{bus_config.get('host')}:{bus_config.get('host')}"
                    
                    args.debug = True if args.debug else config_run.get("debug", False)
                    args.console = True if args.console else config_run.get("console", False)
                    args.nout = True if args.nout else config_run.get("no_output", False)
                    args.filter_case = args.filter_case.split(",") if config_run.get("filter_case") is None and isinstance(args.filter_case, str) else config_run.get("filter_case")

                    config_run_report = config_run.get("report")
                    args.report_html = config_run_report.get("report_html", True)
                    args.report_output_dir = config_run_report.get("report_path")
                    args.report_template = config_run_report.get("report_template", None)
                    args.report_export_template = config_run_report.get("report_export_template", None)
                    args.report_export_dir = config_run_report.get("report_export_path", None)

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

        # here : bus server <- password@host:port
        if args.bus_server:
            if "@" in args.bus_server and ":" in args.bus_server:
                password, temp = args.bus_server.split("@")
                host, port = temp.split(":")
                args.bus_server = [bytes(password, encoding='utf-8'), host, int(port)]

        # here : case <- dir/file
        if args.case:
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
                        print(f"found wrong case path ... {path}")
                        sys.exit(-2)
                else:
                    args.case.append(path)

        # here filter not in config
        if isinstance(args.filter_case, str):
            args.filter_case = args.filter_case.split(',')

        print(args)

        main_program = Program()
        main_program.run(args)
    elif args.all == "init":
        print(args)
        helper = Helper()
        helper.init_workspace()
    elif args.all == "help":
        Helper.print_help()
    else:
        print("Wrong args, using 'python -m haf help' to get the usage information.")


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main_args()