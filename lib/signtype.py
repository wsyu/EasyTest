#!/usr/bin/env python
# encoding: utf-8
"""
@version: python 3.6.3
@author: wsy
@software: PyCharm
@file: signtype.py
@time: 2018/1/30 10:36
"""
import hashlib

def get_sign(sign_type, data, private_key):
    if sign_type == 1:
        return sign_1(data)
    if sign_type == 2:
        return sign_2(data, private_key)
    if sign_type == 3:
        return sign_3(data)

# 签名方式1
def sign_1(data):
    return data

# 签名方式2
def sign_2(data, private_key=''):
    # keys = dic.keys()
    keys = sorted(data.keys())
    temp = ''
    # privateKey = ''
    for key in keys:
        temp += data[key]
    md5 = hashlib.md5()
    temp += private_key
    md5.update(temp.encode(encoding='utf-8'))
    signature = md5.hexdigest()
    data['sign'] = signature
    return data


# 签名方式3
def sign_3(data):
    keys = sorted(data.keys())
    temp = ''
    for key in keys:
        temp += '"' + key + '"' + ':' + '"' + data[key] + '"' + ','
    temp = '{%s}' % temp[:-1]
    md5 = hashlib.md5()
    md5.update(temp.encode(encoding='utf-8'))
    data = md5.hexdigest()
    return data