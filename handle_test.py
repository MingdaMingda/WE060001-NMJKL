#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import tornado.web

import io_weixin_auth

class Test2Handler(tornado.web.RequestHandler):
    def get(self):
        logging.info('AAA: IN test-get')

        code = self.get_argument('code', None)
        token_info = io_weixin_auth.get_user_token_by_code(code)
        user_info = io_weixin_auth.get_user_info_by_token_info(token_info)

        self.render('test_001.html', info=user_info)

    def post(self):
        logging.info('AAA: IN test-post')
        self.render('test_001.html')

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
