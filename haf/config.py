# encoding='utf-8'


# git hub main page of haf
GITHUB_URL_BASE = 'https://github.com/hautof/haf'

# bus server default port,domain, client, authkey
BUS_PORT = 9000
BUS_DOMAIN = u"0.0.0.0"
BUS_CLIENT_DOMAIN = u"127.0.0.1"
BUS_AUTH_KEY = bytes("hafbus", encoding='utf-8')

# web server default port
WEB_SERVER = False
WEB_SERVER_PORT = 8888

# app driver path
APP_DRIVER_PATH = 'http://localhost:4723/wd/hub'

# runner count default = 1
COUNT_RUNNER = 1

# case types [base, webui, httpapi, py, app]
CASE_TYPE_BASE = 0
CASE_TYPE_WEBUI = 1
CASE_TYPE_HTTPAPI = 2
CASE_TYPE_PY = 3
CASE_TYPE_APP = 4

# message type [case, result, api, other]
MESSAGE_TYPE_CASE = 10
MESSAGE_TYPE_RESULT = 11
MESSAGE_TYPE_API_RESULT = 12
MESSAGE_TYPE_OTHER = 13

# signal [start, stop, case-end, result-end, record-end, bus-end]
SIGNAL_START = 20
SIGNAL_STOP = 21
SIGNAL_CASE_END = 22
SIGNAL_RESULT_END = 23
SIGNAL_RECORD_END = 24
SIGNAL_BUS_END = 25
SIGNAL_LOGGER_END = 26

# SIGNAL GROUP
SIGNAL_GROUP = {
    SIGNAL_START: "signal start",
    SIGNAL_STOP: "signal stop",
    SIGNAL_CASE_END: "signal case end",
    SIGNAL_RESULT_END: "signal result end",
    SIGNAL_RECORD_END: "signal record end",
    SIGNAL_BUS_END: "signal bus end",
    SIGNAL_LOGGER_END: "signal logger end"
}

# api method [get, post, put, delete]
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

# case run type [run, not run, skip, run, error]
CASE_CAN_RUN_HERE = 40
CASE_CAN_NOT_RUN_HERE = 41
CASE_SKIP = 42
CASE_RUN = 43
CASE_ERROR = 44

# result [pass, fail, skip, error]
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

# case mark, [base, api, app, web]
CASE_MARK_BASE = 60
CASE_MARK_API = 61
CASE_MARK_APP = 62
CASE_MARK_WEB = 63

# operation of app [click, sendkeys, swipe, other, exists]
OPERATION_APP_CLICK = 70
OPERATION_APP_SENDKEYS = 71
OPERATION_APP_SWIPE = 72
OPERATION_APP_OTHER = 73
OPERATION_APP_EXISTS = 74

OPERATION_APP_GROUP = {
  "click": OPERATION_APP_CLICK,
  "swipe": OPERATION_APP_SWIPE,
  "send_keys": OPERATION_APP_SENDKEYS,
  "other": OPERATION_APP_OTHER,
  "exists": OPERATION_APP_EXISTS
}

OPERATION_APP_ANTI_GROUP = {
  OPERATION_APP_CLICK: "click",
  OPERATION_APP_SWIPE: "swipe",
  OPERATION_APP_SENDKEYS: "send_keys",
  OPERATION_APP_OTHER: "other",
  OPERATION_APP_EXISTS: "exists"
}

# operation of web [click, sendkeys, swipe, other, exists]
OPERATION_WEB_CLICK = 80
OPERATION_WEB_SENDKEYS = 81
OPERATION_WEB_SWIPE = 82
OPERATION_WEB_OTHER = 83
OPERATION_WEB_EXISTS = 84

OPERATION_WEB_GROUP = {
  "click": OPERATION_WEB_CLICK,
  "swipe": OPERATION_WEB_SWIPE,
  "send_keys": OPERATION_WEB_SENDKEYS,
  "other": OPERATION_WEB_OTHER,
  "exists": OPERATION_WEB_EXISTS
}

OPERATION_WEB_ANTI_GROUP = {
  OPERATION_WEB_CLICK: "click",
  OPERATION_WEB_SWIPE: "swipe",
  OPERATION_WEB_SENDKEYS: "send_keys",
  OPERATION_WEB_OTHER: "other",
  OPERATION_WEB_EXISTS: "exists"
}

# log path
LOG_PATH_DEFAULT = "./data"

# version define
MAIN_VERSION = 2
SUB_VERSION = 9
FIX_VERSION = 3
VERSION_TYPE = "haf"
PLATFORM_VERSION = f"{VERSION_TYPE}-{MAIN_VERSION}.{SUB_VERSION}.{FIX_VERSION}"

# banner string
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

# run config schema
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
                        "no_output": {"type": "boolean"},
                        "console": {"type": "boolean"},
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
                        },
                        "case_filter": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["log", "bus", "report", "case", "runner", "recorder", "loader", "web_server"]
                }
            },
            "required": ["name", "run"]
        }
    }
}
