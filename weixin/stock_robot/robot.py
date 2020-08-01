# # -*- encoding: utf-8 -*-
# from __future__ import unicode_literals
# import itchat
# from itchat.content import *
#
# # from .stock_data_query import request_sh
#
# white_list = {
#     '三人搞B敢死小分队': '@@82890bb57e5128e4ee4a5e4cbe55d1e0aa03cb05674b1dcdf730f99790a05138',
#     '阿杜粉丝群': u'@@aa8e60f4eefd6e18665b3732e6d74c668ccbd9d9d0d6b9146fda5289a4939ceb',
#     '测试': u'@@7a1c166d72036f9cd916ab81d7a0b56b34ddc0c90337ebc6ecc6f324f0228ca6',
#     "道可道 非常道": "",
# }
#
#
# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     print(msg)
#     print(msg['User']['UserName'])
#     print(white_list.values())
#     if msg['User']['NickName'] in white_list.keys() or msg['User']['NickName'].startswith("stock"):
#
#         if msg.text.startswith("sh"):
#             # result = request_sh(msg.text)
#             result = "aaa"
#         else:
#             return
#         if result:
#             msg.user.send(u'@%s: %s' % (
#                 msg.actualNickName, result))
#
#
# itchat.auto_login(True)
# itchat.run(True)

import itchat


# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling

@itchat.msg_register('Text')
def text_reply(msg):
    if u'作者' in msg['Text'] or u'主人' in msg['Text']:
        return u'你可以在这里了解他：https://github.com/littlecodersh'
    elif u'源代码' in msg['Text'] or u'获取文件' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'这就是现在机器人后台的代码，是不是很简单呢？'
    elif u'获取图片' in msg['Text']:
        itchat.send('@img@applaud.gif', msg['FromUserName'])  # there should be a picture
    else:
        return msg['Text'] or u'收到：' + msg['Text']


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    return ({'Picture': u'图片', 'Recording': u'录音',
             'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
            u'已下载到本地')  # download function is: msg['Text'](msg['FileName'])


@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友信息：' + msg['Text']['Alias']


@itchat.msg_register('Text', isGroupChat=True)
def group_reply(msg):
    if msg['isAt']:
        return u'@%s\u2005%s' % (msg['ActualNickName'],
                                 msg['Text'] or u'收到：' + msg['Text'])


@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'项目主页：github.com/littlecodersh/ItChat\n'
                    + u'源代码  ：回复源代码\n' + u'图片获取：回复获取图片\n'
                    + u'欢迎Star我的项目关注更新！', msg['RecommendInfo']['UserName'])


itchat.auto_login(True, enableCmdQR=True)
itchat.run()
