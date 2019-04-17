# -*- coding: utf-8 -*-
import time, os
from haf.config import *


class WebBasePage:
    '''
    web base page
    '''
    DEFAULT_TIMEOUT = 3

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, key, value):
        if key == "id":
            ele = self.driver.find_element_by_id(value)
        elif key == "name":
            ele = self.driver.find_element_by_name(value)
        elif key == "xpath":
            ele = self.driver.find_element_by_xpath(value)
        else:
            ele = self.driver.find_element(key, value)
        return ele

    def find_element_by_locator(self, locators):
        for key in locators.keys():
            try:
                return self.find_element(key, locators.get(key))
            except Exception as e:
                print(e)

    def click(self, name):
        e = self.find_element_by_locator(name)
        e.click()

    def send_keys(self, name, keys):
        e = self.find_element_by_locator(name)
        e.clear()
        e.send_keys(keys)

    def ele_exists(self, name):
        try:
            e = self.find_element_by_locator(name)
            return True
        except Exception as e:
            return False

    def swipe(self, d):
        if d == "left":
            self.driver.swipe(50, 1400, 800, 1400, 1000)

        if d == "right":
            self.driver.swipe(800, 1400, 50, 1400, 1000)

        if d == "up":
            self.driver.swipe(500, 50, 500, 1400, 1000)

        if d == "down":
            self.driver.swipe(500, 1400, 500, 50, 1000)


class WebBy(object):
    """
    Set of supported locator strategies.
    """

    ID = "id"
    NAME = "name"
    XPATH = "xpath"

    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"


class WebStage(object):
    def __init__(self):
        self.id = 0
        self.name = ""
        self.operation = ""
        self.path = ""
        self.show_try = True
        self.time_sleep = 5
        self.info = {}
        self.result = "NOT RUN"
        self.run_count = 1
    
    def constructor(self, input: dict={}):
        self.id = input.get("id")
        self.name = input.get("name")
        self.operation = OPERATION_WEB_GROUP[input.get("operation")]
        self.path = input.get("path")
        self.show_try = input.get("try")
        self.info = input.get("info")
        self.time_sleep = input.get("sleep")
        self.run_count = input.get("run_count")

    def deserialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "operation": self.operation,
            "path": self.path,
            "show_try": self.show_try,
            "info": self.info,
            "time_sleep": self.time_sleep,
            "result": self.result,
            "run_count": self.run_count
        }


class WebIds(object):
    def __init__(self):
        self.id = ""
        self.subid = ""
        self.name = ""
        self.web_name = ""

    def constructor(self, inputs:dict={}):
        self.id = inputs.get("id")
        self.subid = inputs.get("subid")
        self.name = inputs.get("name")
        self.web_name = inputs.get("web_name")

    def deserialize(self):
        return {
            "id": self.id,
            "subid": self.subid,
            "name": self.name,
            "web_name": self.web_name
        }


class WebDesiredCaps(object):
    def __init__(self):
        self.platformName = ""
        self.platformVersion = ""
        self.start_url = ""

    def constructor(self, inputs: dict={}):
        self.platformName = inputs.get("platformName")
        self.platformVersion = inputs.get("platformVersion")
        self.start_url = inputs.get("start_url")

    def deserialize(self):
        return {
            "platformName": self.platformName,
            "platformVersion": self.platformVersion,
            "start_url": self.start_url
        }


def web_save_screen_shot(driver, path, name):
    try:
        path = f"{path}/png"
        if not os.path.exists(path):
            os.mkdir(path)
        path_full = f"{path}/{name}.png"
        driver.save_screenshot(path_full)
        return path_full
    except Exception as e:
        print(e)
        return e
