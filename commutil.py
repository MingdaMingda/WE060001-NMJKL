#!/usr/bin/env python
#coding=utf-8

import urllib
import logging
import requests

def pack_url(url, paras):
    paras_encode = urllib.urlencode(paras)
    return '%s?%s' % (url, paras_encode)

def fetch_page(url, timeout=0.500):
    logging.debug('url:%s' % url)
    page = requests.get(url, timeout)

    return page.content

def fetch_page_with_paras(url, paras, timeout=0.500):
    full_url = pack_url(url, paras)
    logging.debug('url:%s' % full_url)
    page = requests.get(full_url, timeout=timeout, verify=False)

    return page.content

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
