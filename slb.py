#!/usr/bin/python
# -*-coding:utf-8 -*-

import base64
import hmac
from hashlib import sha1
import urllib
import time
import uuid
import requests
import shutil


class AliyunMonitor:
    def __init__(self, url):
        self.access_id = 'XXXX'
        self.access_secret = 'XXX'
        self.url = url

    # 签名
    def sign(self, accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''

    # 签名串
        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])    # 使用get请求方法
        h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self, encodeStr):
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode('utf-8').encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format': 'XML',
            'Version': '2014-05-15',
            'AccessKeyId': self.access_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'Timestamp': timestamp,
            'Action': 'SetBackendServers',
            'LoadBalancerId': 'slbid',
            'BackendServers': '[{"ServerId":"ECSid","Weight":"0"},{"ServerId":"ECSid","Weight":"0"}]',

        }

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature

        # return parameters
        url = self.url + "/?" + urllib.urlencode(parameters)
        return url
# SetBackendServers

aliyun = AliyunMonitor("http://slb.aliyuncs.com")
url = aliyun.make_url()
request = requests.get(url)
print(request.text)
