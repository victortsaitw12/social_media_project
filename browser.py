#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

class Browser:

    def __init__(self, domain, loadsecond):
        self.domain = domain
        self.intermit=loadsecond
        options = Options()
        options.add_argument("--window-size=390,844")
        options.add_argument("--disable-notifications")
        service = Service("./chromedriver")
        self.driver = webdriver.Chrome(service=service, options=options)

    def goto(self, path):
        url = self.domain + path
        return self.loadPage(url)

    def xpath_soup(self, element):
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:  # type: bs4.element.Tag
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if 1 == len(siblings) else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, 1) if s is child)
                    )
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    def loadPage(self, url):
        self.driver.get(url)
        self.sleep()
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def click(self, element):
        self.driver.find_element_by_xpath(self.xpath_soup(element)).click()
        self.sleep()
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def scrollDown(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.sleep()
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def sleep(self, sec=None):
        if sec is None:
            second=self.intermit
        time.sleep(second)
