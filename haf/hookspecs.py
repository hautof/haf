import pluggy


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
def publish_to_sql(publish, config, results):
    """publish result to sql

    :param publish : or not
    :param result : publish result
    :return : None
    """