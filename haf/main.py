# encoding='utf-8'

from haf.program import Program

import argparse


def main():
    arg_program = argparse.ArgumentParser(prog="python -m haf", add_help=True)

    sub_all_arg_program = arg_program.add_subparsers(dest="all")

    sub_run_arg_program = sub_all_arg_program.add_parser("run", help="run case, using `python -m haf run ` or `python -m haf` to run all case in local path ")
    sub_run_arg_program.add_argument("--case", "-case", dest="case", type=str, help="run cases wiht -case, path or file would be ok")
    sub_run_arg_program.add_argument("--runner-count", "-rc", dest="runner_count", type=int, default=1, help="runner count, default is 1 runner to run cases, max would be cpus*2")
    sub_run_arg_program.add_argument("--bus-server", "-bs", dest="bus_server", type=str, default=None, help="""default is localhost to run bus server;
                                                                 if is ip or domain, would not run local bus-server, and using ip to connect""")
    sub_run_arg_program.add_argument("--web-server", "-ws", type=bool, help="""default is not run;
                                                                 if is True, would create web server to offer the api and html service;
                                                                """)
    sub_run_arg_program.add_argument("--report-html", "-rh", type=bool, default=True, help="""default is True,to generate html report""")
    sub_run_arg_program.add_argument("--report-output-dir", "-rod", dest="report_output_dir", type=str, default="", help="""default is "", using to generate report to this path""")
    sub_run_arg_program.add_argument("--report-template", "-rt", type=str, default="base", help="""default using base to generate report;
                                                                                                                    customer template is support too""")
    sub_run_arg_program.add_argument("--log-dir", "-ld", type=str, required=True, dest="log_dir", help="""log output dir is needed!""")
    sub_run_arg_program.add_argument("--only-loader", "-ol", type=bool, default=False, dest="only_loader", help="""if true, only start loader""")
    sub_run_arg_program.add_argument("--only-bus", "-ob", type=bool, default=False, dest="only_bus", help="""if true, only start bus""")
    sub_run_arg_program.add_argument("--only-runner", "-or", type=bool, default=False, dest="only_runner", help="""if true, only start runner""")
    sub_run_arg_program.add_argument("--only-recorder", "-ore", type=bool, default=False, dest="only_recorder", help="""if true, only start recorder""")

    args = arg_program.parse_args()
    main_program = Program()

    if args.all == "run":
        if isinstance(args.case, str):
            args.case = [str(case) for case in args.case.split(",")]
        if args.runner_count:
            pass
        if args.bus_server:
            if "@" in args.bus_server and ":" in args.bus_server:
                password, temp = args.bus_server.split("@")
                host, port = temp.split(":")
                args.bus_server = [bytes(password, encoding='utf-8'), host, int(port)]
        if args.web_server:
            pass
        print(args)
        main_program.run(args)
    else:
        argparse.ArgumentError("using python -m haf help to show help infos")


