### haf    
    
    The http api auto test framework. 
    
[![Build Status](https://travis-ci.org/tsbxmw/haf.svg?branch=master)](https://travis-ci.org/tsbxmw/haf)
[![Documentation Status](https://readthedocs.org/projects/haf/badge/?version=latest)](https://haf.readthedocs.io/en/latest/?badge=latest)
                

![report](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/show/report.gif)
![all](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/show/all.gif)


### new features

- now support app-ui cases and generate report

- support mysql result publish

- based on local test runners

- support xlsx,json,yml,py cases

- report generate with html-template

- multi-processes on different machines

- multi-runners

- web-server support restful api based on flask

- only mode : loader/runner/recorder/webserver/bus/logger support


### How to get it

> using pip to get it

```shell
   tsbxmw@ps# pip install haf --upgrade
```

> using git tool to get it

```bash
   tsbxmw@ps# git clone https://github.com/tsbxmw/haf
   tsbxmw@ps# cd haf
   tsbxmw@ps# python setup.py install
```


### How to run

#### local bus mode, using local bus to run all cases

- local bus is without --bus-server(-bs) args, when running the program, the bus would be created

##### modify the config.json in testcases

- change the log_path and report_path and case_path to your own path

```json
    {
      "config":{
        "name": "test",
        "run": {
          "sql_publish": {
            "id": 1,
            "sql_name": "upload",
            "publish": true,
            "host": "192.168.0.200",
            "port": 3306,
            "username": "root",
            "password": "root",
            "database": "haf_publish",
            "protocol": "mysql"
          },
          "log": {
            "log_path": "./data"
          },
          "bus": {
            "only": false,
            "host": "",
            "port": "",
            "auth_key": ""
          },
          "report": {
            "report_path": "./data/report.html"
          },
          "case": [
            {
              "case_path": "./testcases/test.xlsx"
            },
            {
              "case_path": "./testcases/test2.json"
            },
            {
              "case_path": "./testcases/test1.xlsx"
            },
            {
              "case_path": "./testcases/test3.yml"
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
```

##### create testcase

- create xlsx/json/yml/py file with template in testcases/

##### run

- run with config

```shell
    python -m haf run -c=./testcases/config.json
```

- run with args

```shell
    python -m haf run -case=./testcases/test.xlsx,./testcases/test2.json -ld=./data -rh=true -rod=./data/report.html
```

##### when running the app cases

- change the config.json's "report" to add report_template

```json
    "report": 
        {
            "report_template": "base_app",
            "report_path": "./data/report.html"
        }
```

![report-app](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/show/report-app.gif)


##### other run args

- run with multi-runners (4 runners)

```shell
    python -m haf run -rc=4
```

- run with web server 

```shell
    python -m haf run -ws=true
```

- run with only-mode

```shell
    # only loader
    python -m haf run -ol=true
    # only bus
    python -m haf run -ob=true
    # only runner
    python -m haf run -or=true
    # only recorder
    python -m haf run -ore=true
```

- run with third report template

```json
    "report": {
        "report_template": "base_app"
    }
```

- run with mysql publish

```json
    "sql_publish": {
        "id": 1,
        "sql_name": "upload",
        "publish": true,
        "host": "192.168.0.200",
        "port": 3306,
        "username": "root",
        "password": "root",
        "database": "haf_publish",
        "protocol": "mysql"
    }
```

![sql](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/png/haf-publish.png)


### web api server suport

- get loader infos

```bash
    http://localhost:8888/loader
```

- get runner infos

```bash
    http://localhost:8888/runner
```

- get result infos

```bash
    http://localhost:8888/result
```

- get report infos

```bash
    http://localhost:8888/report
```

### FrameWork 

#### Design

![map](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/png/HAF-2.0.0.png)

### Doc

> [doc url](https://github.com/tsbxmw/haf/blob/master/docs/design.md)

> [read the doc](https://haf-doc.readthedocs.io/en/dev-2.2.0/)

> [wiki home](https://github.com/tsbxmw/haf/wiki)

> [Quick Start](https://github.com/tsbxmw/haf/wiki/Quick-Start)

### Release Note

[release note](https://github.com/tsbxmw/haf/blob/master/docs/releasenote.md)