#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import logging
import lxml

import hxcfg
import commutil

from lxml import etree

def redirect_by_wx_auth(redirect_uri, scope=hxcfg.WX_SCOPE_BASIC, state='1'):
    '''
    generate redirect-url of weixin-auth2
    '''
    #appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
    # snsapi_userinfo
    paras = [('appid', hxcfg.WX_APPID), ('redirect_uri', redirect_uri), \
            ('response_type', 'code'), ('scope', scope), ('state', state)]
    paras_encode = urllib.urlencode(paras)
    return ('%s%s%s' % (hxcfg.WX_AUTH_PREFIX, paras_encode, '#wechat_redirect'))

def get_user_token_by_code(code):
    '''
    get user-access-token from WXServer
    Flow: HHS<->WXS
    '''
    if code is None:
        return None

    ### fetch data
    # e.g. https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=APPSECRET&code=CODE&grant_type=authorization_code
    url_prefix = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    paras = [('appid', hxcfg.WX_APPID),
            ('secret', hxcfg.WX_APPSECRET),
            ('code', code),
            ('grant_type', 'authorization_code')]
    page = commutil.fetch_page_with_paras(url_prefix, paras)

    if page is None:
        return None

    ### parse code
    logging.debug('[AAA]')
    logging.debug(page)

    try:
        info = json.loads(page)
    except:
        logging.error('load json error')
        return None

    return info

def get_user_info_by_token_info(token_info):
    '''
    get user-info by token_info from WXServer
    Flow: HHS<->WXS
    '''
    if token_info is None:
        logging.error('token_info is None')
        return None
    if not ('openid' in token_info and 'access_token' in token_info):
        logging.error('invalid token_info')
        return None

    user_info = get_user_info_by_token(token_info['openid'], token_info['access_token'])

    return user_info

def get_user_info_by_token(openid, token):
    '''
    get user-info by token and openid from WXServer
    Flow: HHS<->WXS

    e.g.
    https://api.weixin.qq.com/sns/userinfo?access_token=TOKEN&openid=OPENID&lang=zh_CN
    '''
    ### fetch data
    url_prefix = 'https://api.weixin.qq.com/sns/userinfo'
    paras = [('access_token', token),
            ('openid', openid),
            ('lang', 'zh_CN')]
    page = commutil.fetch_page_with_paras(url_prefix, paras)

    ### parse userinfo
    logging.debug('[AAA]')
    logging.debug(page)

    try:
        user_info = json.loads(page)
    except:
        logging.error('load json error')
        return None

    if user_info is None:
        logging.error('user_info is None')
        return None
    if not 'nickname' in user_info:
        #::notice:: other info check omitted
        logging.error('no nickname in user_info')
        return None

    return user_info

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
