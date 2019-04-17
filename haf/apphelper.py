# -*- coding: utf-8 -*-
'''
file name : apphelper
description : the app case helper
others:
    include BasePage
'''
import time, os
from haf.config import *


class BasePage:
    '''
    the base page of app pages, can be implement by cases
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


class By(object):
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


class Stage(object):
    '''
    stage of app test
    '''
    def __init__(self):
        self.id = 0
        self.name = ""
        self.operation = ""
        self.path = ""
        self.show_try = True
        self.time_sleep = 5
        self.info = {}
        self.result = "NOT RUN"
        self.run_count = 0
    
    def constructor(self, input: dict={}):
        '''

        :param input:
        :return:
        '''
        self.id = input.get("id")
        self.name = input.get("name")
        self.operation = OPERATION_APP_GROUP[input.get("operation")]
        self.path = input.get("path")
        self.show_try = input.get("try")
        self.info = input.get("info")
        self.time_sleep = input.get("sleep")
        self.run_count = input.get("run_count")

    def deserialize(self):
        '''

        :return:
        '''
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


class AppIds(object):
    '''
    ids of app
    '''
    def __init__(self):
        self.id = ""
        self.subid = ""
        self.name = ""
        self.app_name = ""

    def constructor(self, inputs:dict={}):
        '''

        :param inputs:
        :return:
        '''
        self.id = inputs.get("id")
        self.subid = inputs.get("subid")
        self.name = inputs.get("name")
        self.app_name = inputs.get("app_name")

    def deserialize(self):
        '''

        :return:
        '''
        return {
            "id": self.id,
            "subid": self.subid,
            "name": self.name,
            "api_name": self.app_name
        }


class DesiredCaps(object):
    '''
    desired caps needed by appium
    '''
    def __init__(self):
        self.automationName = ""
        self.platformName = ""
        self.platformVersion = ""
        self.deviceName = ""
        self.appPackage = ""
        self.appActivity = ""
        self.noReset = True

    def constructor(self, inputs: dict={}):
        '''

        :param inputs:
        :return:
        '''
        self.automationName = inputs.get("automationName")
        self.platformName = inputs.get("platformName")
        self.platformVersion = inputs.get("platformVersion")
        self.deviceName = inputs.get("deviceName")
        self.appPackage = inputs.get("appPackage")
        self.appActivity = inputs.get("appActivity")
        self.noReset = inputs.get("noReset", True)

    def deserialize(self):
        '''

        :return:
        '''
        return {
            "automationName": self.automationName,
            "platformName": self.platformName,
            "platformVersion": self.platformVersion,
            "deviceName": self.deviceName,
            "appPackage": self.appPackage,
            "appActivity": self.appActivity,
            "noReset": self.noReset
        }


def save_screen_shot(driver, path, name):
    '''
    save the screen shot to the path of the name
    :param driver:
    :param path:
    :param name:
    :return:
    '''
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
