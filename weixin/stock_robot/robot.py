# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import itchat
from itchat.content import *

from weixin.stock_robot.stock_data_query import request_sh

itchat.auto_login(hotReload=True)

white_list = {
    '三人搞B敢死小分队': '@@82890bb57e5128e4ee4a5e4cbe55d1e0aa03cb05674b1dcdf730f99790a05138',
    '股票互利共赢群': u'@@aa8e60f4eefd6e18665b3732e6d74c668ccbd9d9d0d6b9146fda5289a4939ceb',
    '测试': u'@@7a1c166d72036f9cd916ab81d7a0b56b34ddc0c90337ebc6ecc6f324f0228ca6',
    "道可道 非常道": "",
}


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    print(msg)
    print msg['User']['UserName']
    print white_list.values()
    if msg['User']['NickName'] in white_list.keys() or msg['User']['NickName'].startswith("stock"):

        # if " " in msg.text:
        #     prefix, code = msg.text.split(" ")
        # else:
        #     return

        if msg.text.startswith("sh"):
            result = request_sh(msg.text)
        else:
            return
        if result:
            msg.user.send(u'@%s: %s' % (
                msg.actualNickName, result))


itchat.run()
