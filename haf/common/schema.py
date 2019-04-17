'''
file name : schema
description : the json schema check
others:
    usage:
        check_config(config)
'''


from jsonschema import validate
from haf.config import config_schema


def check_config(config):
    '''
    check the haf run config is right or not with the config_schema in haf.config

    :param config: the input
    :return: check result
    '''
    try:
        validate(instance=config, schema=config_schema)
        return True
    except Exception as e:
        print(e)
        return False