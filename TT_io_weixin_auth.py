#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

import io_weixin_auth

def test_get_user_token_by_code():
    #code = '0010bc8ec77f6972b66ad5cb143ceb4i'
    code = '041709e7b1cff6ece362b81e8e071a1j'

    token_info = io_weixin_auth.get_user_token_by_code(code)

    return token_info

def test_get_user_info_by_token(openid, token):
    #openid = 'occ4ovxUED8OWFpV0q5XM98S48wE'
    #token = 'OezXcEiiBSKSxW0eoylIeI6rrU2VFUNTsnm9tD9ZhVfu2jw0MMJ_Osu48gmTq5RUuk2-qh_4W2wZ_EbAkQplGHFihR_p5kmIinEqxK5s-VAwrxi09xB02QuiZLVdMArWhwQ6WLI_wBNOS8ucIZt7uw'
    return io_weixin_auth.get_user_info_by_token(openid, token)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Begin')

    token_info = test_get_user_token_by_code()
    if (not token_info is None) and ('openid' in token_info):
        user_info = test_get_user_info_by_token(token_info['openid'], token_info['access_token'])
        if (not user_info is None) and ('nickname' in user_info):
            logging.info('openid: %s' % user_info['openid'])
            logging.info('nickname: %s' % user_info['nickname'])
            logging.info('headimgurl: %s' % user_info['headimgurl'])
    else:
        logging.error('bad token')

    logging.info('Done')

#/* vim: set ai expandtab ts=4 sw=4 sts=4 tw=100: */
