import importlib


abc = importlib.import_module("thirdparty.corpus_api")
print(abc)
print(getattr(abc, "SqlCheck"))