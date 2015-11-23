#!/usr/bin/env python
#coding=utf-8

import requests

def fetch_page(url, timeout=0.500):
    r = requests.get(url, timeout)
    return r

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
