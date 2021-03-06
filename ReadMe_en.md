# HAF    

    The high automation framework. 

[![Build Status](https://travis-ci.org/hautof/haf.svg?branch=master)](https://travis-ci.org/hautof/haf)
[![Documentation Status](https://readthedocs.org/projects/haf/badge/?version=latest)](https://haf.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/haf.svg)](https://img.shields.io/pypi/v/haf.svg) [![GitHub release](https://img.shields.io/github/release/hautof/haf.svg)](https://img.shields.io/github/release/hautof/haf.svg)
                

![all](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/show/all.gif)


# How to get it

## using pip to get it

```shell
   tsbxmw@ps# pip install haf --upgrade
```

## using git tool to get it

```bash
   tsbxmw@ps# git clone https://github.com/tsbxmw/haf
   tsbxmw@ps# cd haf
   tsbxmw@ps# python setup.py install
```


# How to run

## 1 using init to init workspace

```bash
    python -m haf init
```

or 

```bash
    git clone https://github.com/tsbxmw/haf-sample
```

## 2 run it in dir haf-sample

### run api case

```bash
    python -m haf run -c=config.json
```

### run web ui case

```bash
    python -m haf run -c=config-web.json
```

## 3 find the report at the data dir

    using chrome or other browsers to open the html file

# Others

| quick start | haf-sample | pypi | read the doc |
|---|---|---|---|
| [start](https://github.com/tsbxmw/haf/wiki/Quick-Start) | [haf-sample](https://github.com/hautof/haf-sample) | [pypi](https://pypi.org/project/haf/) | [doc](https://haf-doc.readthedocs.io/en/dev-2.1.0/) |


# Plugins

| id | plugin name | version | git hub repo|
|---|---|---|---|
| 1 | haf api server | [![PyPI](https://img.shields.io/pypi/v/hafapiserver.svg)](https://img.shields.io/pypi/v/hafapiserver.svg) | [haf webserver](https://github.com/hautof/haf-plugin-webserver) |
| 2 | haf sql publish | [![PyPI](https://img.shields.io/pypi/v/hafsqlpublish.svg)](https://img.shields.io/pypi/v/hafsqlpublish.svg) | [haf sqlpublish](https://github.com/hautof/haf-plugin-sqlpublish) |


# How to run your define cases

## Other running locally

### Local bus mode, using local bus to run all cases

- local bus is without --bus-server(-bs) args, when running the program, the bus would be created

### modify the config.json in testcases

- change the `log_path` and `report_path` and `case_path` to your own path
- delete `config->run->sql_publish` if you don't have an haf-publish

```json
    {
      "config":{
        "name": "test",
        "debug" : false,
        "bus_server_port": 8801,
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
            "report_path": "./data/report.html",
            "report_template": "base",
            "report_export_path": "email"
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

### create testcase or using default cases

- create xlsx/json/yml/py file with template in testcases/
- using haf-sample case template

### run

#### run with config

```shell
    python -m haf run -c=./testcases/config.json
```

#### run with args

```shell
    python -m haf run -case=./testcases/test.xlsx,./testcases/test2.json -ld=./data -rh=true -rod=./data/report.html
```

# when running the api cases


![report](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/show/report.gif)



# when running the app cases

- change the config.json's "report" to add report_template

```json
    "run": {
        "type": "app"  # change type to app

        "report": {
            "report_template": "base_app",  # change report_template to base_app
            "report_path": "./data/report.html"
        }
    }
```

![report-app](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/show/report-app.gif)


# when runnng the web ui cases

- change the config.json's "report" to add report_template


```json
    "run": {
        "type": "web"  # change type to web

        "report": {
            "report_template": "base_web",  # change report_template to base_web
            "report_path": "./data/report.html"
        }
    }
```

![report-app](https://raw.githubusercontent.com/tsbxmw/haf/master/docs/show/webui.gif)



# haf samples

> https://github.com/hautof/haf-sample


# other run args

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


### now hafweb support 

```bash
    tsbx# pip install hafweb -U
```


```python
    python -m hafweb -ss=root:root@localhost:3306@haf_publish -p=8081
```

- default page

   http://localhost:8081/

- index page
   
   http://localhost:8081/index
   
- today page

   http://localhost:8081/today
   
- others support looking at hafweb project


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
    http://localhost:8888/report-app
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

### new features

- now support app-ui/web-ui cases and generate report

- support mysql result publish

- based on local test runners

- support xlsx,json,yml,py cases

- report generate with html-template

- multi-processes on different machines

- multi-runners

- web-server support restful api based on flask

- only mode : loader/runner/recorder/webserver/bus/logger support