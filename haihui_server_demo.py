#!/usr/bin/env python
#coding=utf-8
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.auth
import os
import sys
import logging

from io_weixin import IO_Weixin_ValidateHandler
from handle_test import Test2Handler
from tornado.options import define, options
from tornado import gen

define("port", default=80, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("su")
        if not user_json: 
            return None
        return tornado.escape.json_decode(user_json)

class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
	user = self.current_user
        self.render('index.html', user=user)

    def post(self):
        openid = self.get_argument("openid")
        user = {
            'openid' : openid,
            }
        self.set_secure_cookie("su", tornado.escape.json_encode(user))
        self.set_cookie("us", openid)
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("su")
        self.clear_cookie("us")
        self.write("Byebye~")

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        [
            (r"/", LoginHandler),
            (r"/io/weixin/", IO_Weixin_ValidateHandler),
            (r"/test/", Test2Handler),
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        #xsrf_cookies=True,
        cookie_secret="WeLcOmToHaIhUi",
        login_url="/auth/login",
        debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    sys.stderr.write('[trace] service started...\n')

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
