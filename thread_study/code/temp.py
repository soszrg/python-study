# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import os
from time import sleep

import requests

refreshToken = "http://127.0.0.1:8004/enduser/refreshToken/"

login = False
if login:
    res = requests.post("http://127.0.0.1:8004/enduser/login/", data={"appid": "5cdb7ebc-32bd-11e6-a739-00163e0204c0", "loginname": "17612118938", "password": "123456"})
    res_dict = json.loads(res.text)
    base_token = res_dict["token"]
    print base_token
    exit()
base_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmlnX2lhdCI6MTQ5MjQ3NzYwNSwiaWRlbnRpZmljYXRpb24iOiIxNzYxMjExODkzOCIsImV4cCI6MTQ5MjQ3NzkwNSwiYXBwaWQiOiI1Y2RiN2ViYy0zMmJkLTExZTYtYTczOS0wMDE2M2UwMjA0YzAiLCJ1c2VyX2lkIjo3LCJlbmR1c2VyaWQiOiI0ZmRjZWUwMC0xMmJjLTExZTctYmQ2Mi1kYzUzNjAxNzUyM2IifQ.k_Zx6l9trDM88j7kWZ0PXkAhZNiMU6v2VVV1Esci0hM"

while(True):
    print "="*20, "base_token", "="*20
    print base_token

    res = requests.post(url=refreshToken, data={"token": base_token})
    res_dict = json.loads(res.text)
    print res_dict
    new_token = res_dict["token"]
    print "=" * 20, "refresh_token", "=" * 20
    print new_token
    res = requests.get("http://127.0.0.1:8004/enduser/devicelistbyenduser/", headers={"Authorization": "jwt %s" % new_token})
    print res.text
    base_token = new_token
    sleep(10)
