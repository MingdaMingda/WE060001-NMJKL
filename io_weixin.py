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

from lxml import etree

class IO_Weixin_ValidateHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info('[AAA] into get')

        if not self.check_wx_signature():
            return;

    def packmsg(self, msg):
        if msg is None or (not type(msg) is types.DictType):
            return '<xml></xml>'

        s = ['<xml>']

        for key in msg:
            value = msg[key]
            if type(value) is types.IntType:
                s.append('<%s>%d</%s>' % (key, value, key))
            if type(value) is types.StringType:
                s.append('<%s><![CDATA][%s]]></%s>' % (key, value, key))
            if type(value) is types.UnicodeType:
                s.append('<%s><![CDATA][%s]]></%s>' % (key, value.encode('utf-8'), key))
        s.append('</xml>')

        p = '\n'.join(s)

        return p

    def post(self):
        logging.info('[AAA] into post')

        str_xml = self.request.body
        xml = etree.fromstring(str_xml) 

        logging.info('[AAA]')
        logging.info(str_xml)

        response = {
            'FromUserName': xml.find("ToUserName").text,
            'ToUserName': xml.find("FromUserName").text,
            'CreateTime' : int(time.time()),
            'MsgType' : 'text',
            'Content' : 'Hi~%s' % (xml.find("Content").text),
        }

        self.render('wx_reply_text.html', info=response)

    def check_wx_signature(self):
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echostr = self.get_argument('echostr', '')

        token = 'hNtQGASCHcAJAISX'

        arr = [token, timestamp, nonce]
        arr.sort()

        s = ''.join(arr)
        s1 = hashlib.sha1(s).hexdigest()

        #self.write('siga:%s<br>time:%s<br>nonce:%s<br><br>s:%s<br>s1:%s<br>' % (signature, timestamp, nonce, s, s1))

        if s1 == signature:
            self.write(echostr)
            return True
        else:
            self.write('error')
            return False

class IO_Weixin_Handler(tornado.web.RequestHandler):
    def get(self):
        self.check_wx_signature()

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
