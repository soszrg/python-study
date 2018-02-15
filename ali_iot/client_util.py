# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from aliyunsdkcore import client


class ClientUtil:
    def __init__(self):
        pass

    @staticmethod
    def create_client():
        # 阿里云账号
        access_key_id = 'LTAI4O7s8tyyJnip'
        access_key_secret = 'AjpahEowqJFJSZohp6QktStiComaQP'
        region_id = 'cn-shanghai'
        clt = client.AcsClient(access_key_id, access_key_secret, region_id)
        return clt
