from jsonschema import validate
from haf.config import config_schema

def check_config(config):
    try:
        validate(instance=config, schema=config_schema)
        return True
    except Exception as e:
        print(e)
        return False