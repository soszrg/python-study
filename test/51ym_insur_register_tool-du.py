# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
import re

import datetime
import requests
import time

token = "00385737d47257a2b3eb1f05afdfbb825175fb25"
item_id = "14512"
account_count = 0
du = 1471
cui = 1199
wo = 1323
invite_id = du
errors = 0

while True:
    try:
        # 获取电话号码
        print "="*50
        print "====>fetch phone number"
        fetch_phone_url = "http://api.51ym.me/UserInterface.aspx?action=getmobile&itemid=%s&token=%s" % (item_id, token)
        phone_res = requests.get(fetch_phone_url)
        print phone_res.status_code
        print phone_res.text
        phone = phone_res.text.split("|")[1]
        print "phone==>%s" % phone

        # 发送验证码
        print "="*50
        print "====>send msg"
        send_msg = "https://wallet.qusukj.com/api/v1/login/sms"
        send_res = requests.post(send_msg, data={"telephone": phone})
        print send_res.status_code
        print send_res.text

        # 获取验证码
        print "="*50
        print "====>fetch msg code"
        fetch_msg_url = "http://api.51ym.me/UserInterface.aspx?action=getsms&mobile=%s&itemid=%s&token=%s&release=1" \
                        % (phone, item_id, token)
        msg_res = None
        count = 0
        while True:
            time.sleep(5)
            msg_res = requests.get(fetch_msg_url)
            count += 1
            if (msg_res.status_code == 200 and msg_res.text != "3001") or count > 12:
                break

        if msg_res and msg_res.status_code==200 and msg_res.text != "3001":
            print msg_res.text
            code = re.findall("\d{6}", msg_res.text)
            print "code==>%s" % code
        else:
            errors += 1
            print "fetch code error"
            continue

        # 注册账户
        print "="*50
        print "====>register account"
        register_url = "https://wallet.qusukj.com/api/v1/user/login"
        reg_res = requests.post(register_url, data={"telephone": phone, "inviter_id": invite_id, "smsCode": code})
        print reg_res.status_code
        print reg_res.text

        if reg_res.status_code == 200:
            print "=" * 50
            print "===> new user register ok!"
            print "=" * 50
            account_count += 1
        else:
            errors += 1
            print "register error"
        print "===> has registered %d users" % account_count
        if account_count < 100:
            rand_number = random.randint(1, 3)
        elif account_count < 200:
            rand_number = random.randint(10, 60)
        else:
            rand_number = random.randint(60, 600)
        print "[%s]===> will wait for %d minutes to another register" % (datetime.datetime.now(), rand_number)
        time.sleep(60 * rand_number)
    except Exception as e:
        print e.message
        continue
