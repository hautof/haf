import itertools
import random

import pluggy
import json
import os
import sys
import argparse
from haf import hookspecs, lib


class PluginManager(object):
    '''
    plugin manager
    now have : add_option before main()
            : load_from_file at loader
            : publish_to_sql after test
            : start_web_server at program begining
    '''
    def __init__(self):
        self.get_plugin_manager()

    def add_options(self, sub_run_arg_program):
        pm = self.pm
        return pm.hook.add_option(parse = sub_run_arg_program)

    def load_from_file(self, file_name):
        pm = self.pm
        inputs = pm.hook.load_from_file(file_name = file_name)
        if isinstance(inputs, list):
            return inputs[0]
        elif isinstance(inputs, dict):
            return inputs

    def publish_to_sql(self, args, results):
        pm = self.pm
        publish_result = pm.hook.publish_to_sql(args=args, results=results)
        return publish_result

    def start_web_server(self, args, bus_client):
        pm = self.pm
        result = pm.hook.start_web_server(args=args, bus_client=bus_client)
        return result

    def get_plugin_manager(self):
        self.pm = pluggy.PluginManager("haf")
        self.pm.add_hookspecs(hookspecs)
        self.pm.load_setuptools_entrypoints("haf")
        self.pm.register(lib)
        return self.pm


plugin_manager = PluginManager()