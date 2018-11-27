# encoding='utf-8'

from haf.program import Program

import argparse


def main():
    arg_program = argparse.ArgumentParser(prog="python -m haf", add_help=True)

    sub_all_arg_program = arg_program.add_subparsers(dest="all")

    sub_run_arg_program = sub_all_arg_program.add_parser("run", help="run case, using `python -m haf run ` or `python -m haf` to run all case in local path ")
    sub_run_arg_program.add_argument("--case", "-case", dest="case", help="run cases wiht -case, path or file would be ok")
    sub_run_arg_program.add_argument("--runner-count", "-rc", dest="runner_count", type=int, default=1, help="runner count, default is 1 runner to run cases, max would be cpus*2")
    sub_run_arg_program.add_argument("--bus-server", "-bs", dest="bus_server", type=str, help="""default is localhost to run bus server;
                                                                 if is ip or domain, would not run local bus-server, and using ip to connect""")
    sub_run_arg_program.add_argument("--web-server", "-ws", type=bool, help="""default is not run;
                                                                 if is True, would create web server to offer the api and html service;
                                                                """)
    sub_run_arg_program.add_argument("--report-html", "-rh", type=bool, required=True, default=True, help="""default is True,to generate html report""")
    sub_run_arg_program.add_argument("--report-output-dir", "-rod", type=str, required=False, default="", help="""default is "", using to generate report to this path""")
    sub_run_arg_program.add_argument("--report-template", "-rt", type=str, default="base", help="""default using base to generate report;
                                                                                                                    customer template is support too""")
    args = arg_program.parse_args()
    main_program = Program()

    if args.all == "run":
        if args.case:
            pass
        if args.runner_count:
            pass
        if args.bus_server:
            pass
        if args.web_server:
            pass

        main_program.run(args)
    else:
        argparse.ArgumentError("using python -m haf help to show help infos")


