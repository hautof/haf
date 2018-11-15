# haf    
    
    The auto test framework. 
    
[![Build Status](https://travis-ci.org/tsbxmw/haf.svg?branch=master)](https://travis-ci.org/tsbxmw/haf)


> based on pytest & allure

> xlsx easy cases

## How to get it

```shell
    pip install haf --upgrade
```

## How to run

### mkdir at testcases

```shell
    mkdir testcases
```

### create xlsx file 

### move file.xlsx to testcases

### run 

```shell
    python -m haf --case=testcases
```

## 可能用到的知识

> git : 获取代码 https://git-scm.com/book/zh/v2/

> python : http://www.runoob.com/python3/python3-tutorial.html

> cmd : https://www.cnblogs.com/accumulater/p/7110811.html

> allure-pytest : 生成报告 https://docs.qameta.io/allure/#_pytest

> pytest : python测试框架 http://www.pytest.org/

> tomcat : web 框架

> mysql : mysql 数据库

> sqlserver : mssql 数据库

> http method : http操作方法 http://www.runoob.com/http/http-tutorial.html

> others ... 



## FrameWork 

### Design

### Class

### Doc

## Release Note

### version 1.1.6

* add argparse to make arg tool
* local runner to replace pytest (dev)
* testsuite support (dev)
* testresult support (dev)

### version 1.1.5

* add assertpy support

### version 1.1.3

* add assert_that func to Run to show more in allure

### version 1.1.1

* change to wheel 

### version 1.0.2

* upload to pypi

### version 0.5

* 增加 report allure 2.5 setup 支持
* 增加 report 的 发布


### version 0.4

* complete basic function with xlsx file 
* add python doc support at doc 