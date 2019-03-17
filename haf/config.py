# encoding='utf-8'

GITHUB_URL_BASE = 'https://github.com/tsbxmw/haf'

BUS_PORT = 9000
BUS_DOMAIN = u"0.0.0.0"
BUS_CLIENT_DOMAIN = u"127.0.0.1"
BUS_AUTH_KEY = bytes("hafbus", encoding='utf-8')

WEB_SERVER = False
WEB_SERVER_PORT = 8888

APP_DRIVER_PATH = 'http://localhost:4723/wd/hub'

COUNT_RUNNER = 1

CASE_TYPE_BASE = 0
CASE_TYPE_WEBUI = 1
CASE_TYPE_HTTPAPI = 2
CASE_TYPE_PY = 3
CASE_TYPE_APP = 4

MESSAGE_TYPE_CASE = 10
MESSAGE_TYPE_RESULT = 11
MESSAGE_TYPE_API_RESULT = 12
MESSAGE_TYPE_OTHER = 13

SIGNAL_START = 20
SIGNAL_STOP = 21
SIGNAL_CASE_END = 22
SIGNAL_RESULT_END = 23
SIGNAL_RECORD_END = 24
SIGNAL_BUS_END = 25

CASE_HTTP_API_METHOD_GET = 30
CASE_HTTP_API_METHOD_POST = 31
CASE_HTTP_API_METHOD_PUT= 32
CASE_HTTP_API_METHOD_DELETE = 33

METHOD_GROUP = {
    "30": "GET",
    "31": "POST",
    "32": "PUT",
    "33": "DELETE"
}

CASE_CAN_RUN_HERE = 40
CASE_CAN_NOT_RUN_HERE = 41
CASE_SKIP = 42
CASE_RUN = 43
CASE_ERROR = 44

RESULT_PASS = 50
RESULT_FAIL = 51
RESULT_SKIP = 52
RESULT_ERROR = 53

RESULT_GROUP = {
    "50": "PASS",
    "51": "FAIL",
    "52": "SKIP",
    "53": "ERROR"
}

CASE_MARK_BASE = 60
CASE_MARK_API = 61
CASE_MARK_APP = 62
CASE_MARK_WEB = 63

OPERATION_APP_CLICK = 70
OPERATION_APP_SENDKEYS = 71
OPERATION_APP_SWIPE = 72
OPERATION_APP_OTHER = 73

OPERATION_APP_GROUP = {
  "click": OPERATION_APP_CLICK,
  "swipe": OPERATION_APP_SWIPE,
  "send_keys": OPERATION_APP_SENDKEYS,
  "other": OPERATION_APP_OTHER
}

OPERATION_APP_ANTI_GROUP = {
  OPERATION_APP_CLICK: "click",
  OPERATION_APP_SWIPE: "swipe",
  OPERATION_APP_SENDKEYS: "send_keys",
  OPERATION_APP_OTHER: "other"
}

OPERATION_WEB_CLICK = 80
OPERATION_WEB_SENDKEYS = 81
OPERATION_WEB_SWIPE = 82
OPERATION_WEB_OTHER = 83

OPERATION_WEB_GROUP = {
  "click": OPERATION_WEB_CLICK,
  "swipe": OPERATION_WEB_SWIPE,
  "send_keys": OPERATION_WEB_SENDKEYS,
  "other": OPERATION_WEB_OTHER
}

OPERATION_WEB_ANTI_GROUP = {
  OPERATION_WEB_CLICK: "click",
  OPERATION_WEB_SWIPE: "swipe",
  OPERATION_WEB_SENDKEYS: "send_keys",
  OPERATION_WEB_OTHER: "other"
}

LOG_PATH_DEFAULT = "D:\workspace\mine\python\haf\data"

MAIN_VERSION = 2
SUB_VERSION = 6
FIX_VERSION = 7
VERSION_TYPE = "haf"
PLATFORM_VERSION = f"{VERSION_TYPE}-{MAIN_VERSION}.{SUB_VERSION}.{FIX_VERSION}"

BANNER_STRS = f"""
  .                     ____
 /\\\\  | |  | | ____    /. _/
( ( ) | |__| |/ __ \___| |___  
 \\\\/  |  __  | (__\  __   ___|
  '   | |  | |\______\ | |   
      |_|  |_| v{MAIN_VERSION}.{SUB_VERSION}.{FIX_VERSION}  |_|
"""

BANNER_STRS_EXIT = f"""
  .                     ____
 /\\\\  | |  | | ____    /. _/
( ( ) | |__| |/ __ \___| |___  
 \\\\/  |  __  | (__\  __   ___|
  '   | |  | |\______\ | |   
      |_|  |_| v{MAIN_VERSION}.{SUB_VERSION}.{FIX_VERSION}  |_|   EXIT
"""

config_schema = {
    "type": "object",
    "properties": {
        "config": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "run": {
                    "type": "object",
                    "properties": {
                        "bus_server_port": {"type": "number"},
                        "sql_publish": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "number"},
                                "sql_name": {"type": "string"},
                                "publish": {"type": "boolean"},
                                "host": {"type": "string"},
                                "port": {"type": "number"},
                                "username": {"type": "string"},
                                "password": {"type": "string"},
                                "database": {"type": "string"},
                                "protocol": {"enum": ["mysql", "mssql"]}
                            },
                            "required": ["id", "sql_name", "publish", "host", "port", "username", "password", "database", "protocol"]
                        },
                        "log":{
                            "type": "object",
                            "properties": {
                                "log_path": {"type": "string"}
                            },
                            "required": ["log_path"]
                        },
                        "bus":{
                            "type": "object",
                            "properties": {
                                "only": {"type": "boolean"},
                                "host": {"type": "string"},
                                "port": {
                                    "oneOf": [
                                        {"type": "string"},
                                        {"type": "number"}
                                    ]
                                },
                                "auth_key": {"type": "string"}
                            },
                            "required": ["only", "host", "port", "auth_key"]
                        },
                        "report":{
                            "type": "object",
                            "properties": {
                                "report_path": {"type": "string"},
                                "report_template": {"type": "string"},
                                "report_export_path": {"type": "string"}
                            },
                            "required": ["report_path"]
                        },
                        "case":{
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "case_path": {"type": "string"}
                                },
                                "required": ["case_path"]
                            }
                        },
                        "runner":{
                            "type": "object",
                            "properties": {
                                "only": {"type": "boolean"},
                                "count": {"type": "number"}
                            },
                            "required": ["only", "count"]
                        },
                        "loader":{
                            "type": "object",
                            "propertied": {
                                "only": {"type": "boolean"}
                            },
                            "required": ["only"]
                        },
                        "recorder":{
                            "type": "object",
                            "propertied": {
                                "only": {"type": "boolean"}
                            },
                            "required": ["only"]
                        },
                        "web_server":{
                            "type": "object",
                            "propertied": {
                                "only": {"type": "boolean"},
                                "port": {
                                    "oneOf": [
                                        {"type": "string"},
                                        {"type": "number"}
                                    ]
                                },
                                "host": {"type": "string"},
                                "run": {"type": "boolean"}
                            },
                            "required": ["run"]
                        }
                    },
                    "required": ["log", "bus", "report", "case", "runner", "recorder", "loader", "web_server"]
                }
            },
            "required": ["name", "run"]
        }
    }
}
