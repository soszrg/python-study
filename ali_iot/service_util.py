# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64
import uuid
import string
import random


class ServiceUtil:

    def __init__(self):
        pass

    # 生成num个随机设备名称，名称为uuid的base64编码，保证唯一性
    @staticmethod
    def device_name_generator(num):
        name_list = []
        while num > 0:
            name_list.append(base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2])
            num -= 1
        name_list = list(set(name_list))
        print "***********namelist cout :", len(name_list)
        # print name_list
        return name_list

    @staticmethod
    def product_name_generator():
        return 'product' + id_generator()


def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '_+'):
    return ''.join(random.choice(chars) for _ in range(size))
