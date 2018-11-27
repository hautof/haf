### haf    
    
    The http api auto test framework. 
    
[![Build Status](https://travis-ci.org/tsbxmw/haf.svg?branch=master)](https://travis-ci.org/tsbxmw/haf)


### new features


- based on local test runner 

- support xlsx,json,yml,py cases

- report generate with html-template

- multi-processes on different machines

- multi-runners

- web-server support restful api based on flask



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

- mkdir at testcases

```shell
    mkdir testcases
```

- create xlsx file with template in testcases/test.xlsx

- move file.xlsx to testcases

- run wit 4 runners and web-server

```shell
    python -m haf run -rc=4 -ws=True --case=testcases/file.xlsx
```


### FrameWork 

#### Design

![map](/doc/HAF-dev2.0.0.png)

#### Doc

[doc url](https://github.com/tsbxmw/haf/tree/dev-2.0.0/doc)

### Release Note

[release note](https://github.com/tsbxmw/haf/tree/dev-2.0.0/releasenote.md)