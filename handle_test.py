#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import hashlib
import logging
import time
import types

import lxml
import xmltodict
import tornado.web

class Test2Handler(tornado.web.RequestHandler):
    def get(self):
        logging.info('AAA: IN test-get')
        self.render('test_001.html')

    def post(self):
        logging.info('AAA: IN test-post')
        self.render('test_001.html')

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
