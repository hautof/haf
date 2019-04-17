'''
lib
'''

import haf
from haf.utils import LoadFromConfig
from haf.common.log import Log

logger = Log.getLogger(__name__)


@haf.hookimpl
def add_option():
    '''
    add option to run program
    :return:
    '''
    args = []
    return args


@haf.hookimpl
def load_from_file(file_name):
    '''
    u can rewrite this in plugin to overwrite the hooks
    :param file_name:
    :return:
    '''
    if file_name.endswith(".xlsx"):
        output = LoadFromConfig.load_from_xlsx(file_name)
    elif file_name.endswith(".json"):
        output = LoadFromConfig.load_from_json(file_name)
    elif file_name.endswith(".yml"):
        output = LoadFromConfig.load_from_yml(file_name)
    elif file_name.endswith(".py"):
        output = LoadFromConfig.load_from_py(file_name)
    return output


@haf.hookimpl
def publish_to_sql(args, results):
    pass


@haf.hookimpl
def start_web_server(args, bus_client):
    return False