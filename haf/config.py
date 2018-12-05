# encoding='utf-8'


BUS_PORT = 9000
BUS_DOMAIN = u"0.0.0.0"
BUS_AUTH_KEY = bytes("hafbus", encoding='utf-8')

WEB_SERVER = False
WEB_SERVER_PORT = 8888

COUNT_RUNNER = 1

CASE_TYPE_BASE = 0
CASE_TYPE_WEBUI = 1
CASE_TYPE_HTTPAPI = 2
CASE_TYPE_PY = 3

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

LOG_PATH_DEFAULT = "D:\workspace\mine\python\haf\data"

MAIN_VERSION = 2
SUB_VERSION = 0
FIX_VERSION = 3
VERSION_TYPE = "dev"
PLATFORM_VERSION = f"{VERSION_TYPE}-{MAIN_VERSION}.{SUB_VERSION}.{FIX_VERSION}"

BANNER_STRS =f"""
***************************************
*    H      H      A      FFFFFFFF    *
*    H      H     A A     F           *
*    H      H    A   A    F           *
*    HHHHHHHH   AAAAAAA   FFFFFFFF    *
*    H      H  A       A  F           *
*    H      H A         A F           *
*    H      HA           AF    v{MAIN_VERSION}.{SUB_VERSION}.{FIX_VERSION} *
***************************************
"""