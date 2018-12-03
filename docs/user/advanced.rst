.. _advanced:

Advanced Usage
==============

.. image:: https://travis-ci.org/tsbxmw/haf.svg?branch=dev-2.1.0
    :target: https://travis-ci.org/tsbxmw/haf

.. image:: https://raw.githubusercontent.com/tsbxmw/haf/dev-2.1.0/docs/show/all.gif

.. image:: https://raw.githubusercontent.com/tsbxmw/haf/dev-2.1.0/docs/show/report.gif


How to get it
==============

- using pip to get it::

    $tsbxmw@ps# pip install haf --upgrade

- using git tool to get it::

    $tsbxmw@ps# git clone https://github.com/tsbxmw/haf
    $tsbxmw@ps# cd haf
    $tsbxmw@ps# python setup.py install

How to run
==============

- local bus mode, using local bus to run all cases

    local bus is without --bus-server(-bs) args, when running the program, the bus would be created

- modify the config.json in testcases

    change the log_path and report_path and case_path to your own path::

      {
      "config":{
        "run": {
          "log": {
            "log_path": "D:/workspace/mine/python/haf/data"
          },
          "bus": {
            "only": false,
            "host": "",
            "port": "",
            "auth_key": ""
          },
          "report": {
            "report_path": "D:/workspace/mine/python/haf/data/report.html"
          },
          "case": [
            {
              "case_path": "D:/workspace/mine/python/haf/testcases/test.xlsx"
            },
            {
              "case_path": "D:/workspace/mine/python/haf/testcases/test2.json"
            },
            {
              "case_path": "D:/workspace/mine/python/haf/testcases/test1.xlsx"
            },
            {
              "case_path": "D:/workspace/mine/python/haf/testcases/test3.yml"
            }
          ],
          "runner":{
            "only": false,
            "count": 4
          },
          "loader": {
            "only": false
          },
          "recorder": {
            "only": false
          },
          "web_server": {
            "host": "",
            "port": "",
            "run": true
          }
        }
      }

    }

- create testcase

    create xlsx/json/yml file with template in testcases/

- run

 + run with config::

    python -m haf run -c=./testcases/config.json

 + run with args::

     python -m haf run -case=./testcases/test.xlsx,./testcases/test2.json -ld=./data -rh=true -rod=./data/report.html


- other run args

 + run with multi-runners (4 runners)::

    python -m haf run -rc=4

 + run with web server::

    python -m haf run -ws=true

 + run with only-mode::

    # only loader
    python -m haf run -ol=true
    # only bus
    python -m haf run -ob=true
    # only runner
    python -m haf run -or=true
    # only recorder
    python -m haf run -ore=true

- web api server suport

 + get loader infos

    http://localhost:8888/loader

 + get runner infos

    http://localhost:8888/runner

 + get result infos

    http://localhost:8888/result

 + get report infos

    http://localhost:8888/report



