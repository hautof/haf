import pluggy
'''
hookspecs
'''

hookspec = pluggy.HookspecMarker("haf")


@hookspec
def add_option(parse):
    """add option to parse

    :param run args
    :return: None
    """


@hookspec
def load_from_file(file_name):
    """add option to parse

    :param run args
    :return: file_name
    """


@hookspec
def publish_to_sql(args, results):
    """publish result to sql

    :param publish : or not
    :param result : publish result
    :return : None
    """

@hookspec
def start_web_server(args, bus_client):
    """start web server

    :param args:
    :return:
    """