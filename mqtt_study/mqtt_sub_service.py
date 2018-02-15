# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import paho.mqtt.client as mqtt
import json

import time

user = "pri_shuyi@linkdotter.com"
pwd = "123456"
topic = "d2p/50880e3e-5b05-11e7-9baf-00163e120d98/#"
endpoint = "mqtt.fogcloud.io"  # 地址
port = 1883  # endpoint端口

#db = MySQLdb.connect(host='127.0.0.1', port=3306, user='health', passwd='health654+_)', db='health')


def save_payload_to_db(topic, payload):
    #cursor = db.cursor()

    # cursor.execute("SELECT VERSION()")
    # data = cursor.fetchone()
    # print "database version is %s\n" %data  #打印数据库版本，可以删除
    # print(payload)
    # print(topic)

    code = topic.split("/")[2]
    device = topic.split("/")[1]

    # print(code)
    # print(device)

    try:
        payload = json.loads(payload)
        # print(payload["command_id"])
        # print(payload["CMD"])
        if type(payload) is not dict:
            print(payload)
        '''
        heart = payload["G"][0]['D']
        breathed = payload["G"][1]['D']
        gateo = payload["G"][2]['D']
        gatem = payload["G"][3]['D']
        turnover = payload["G"][5]['D']
        isbed = payload["G"][4]['D']

        mystr = "'" + str(code) + "','" + str(device) + "','" + str(breathed) + "','" + str(heart) + "','" + str(
            gateo) + "','" + str(gatem) + "','" + str(turnover) + "','" + str(isbed) + "'," + str(time.time())
        tb = "lt_monitor" + str(time.strftime("%Y%m%d"))
        sql = """INSERT INTO %s(`code`,`device`,`breathed`,`heart`,`gateo`,`gatem`,`turnover`,`isbed`,`addtime`) VALUES (%s)""" % (
        tb, mystr)  # payload内容整体插入到数据库中
        '''
        try:
            print(payload)
            #cursor.execute(sql)  # 插入数据库，表名称为IT_MONITOR的表
            #db.commit()
        except:
            print "insert data with error and then rollback"
            #db.rollback()

    except:
        print "payload data error"


def on_connect(client, userdata, flags, rc):  # 连接后返回0为成功
    print("[%s]Connected with result code " % datetime.datetime.now() + str(rc))
    if rc == 0:
        print "[%s]Connected ok!" % datetime.datetime.now()
        client.subscribe(topic, qos=1)  # qos
    else:
        print "[%s]Connected error, Please restart service!" % datetime.datetime.now()
        exit()


def on_disconnect(client, userdata, rc):
    print("[%s]Disconnect with code: " % datetime.datetime.now() + str(rc))


def on_message(client, userdata, msg):
    print("[%s]Topic:" % datetime.datetime.now() + msg.topic + " Message:" + str(msg.payload))
    # save_payload_to_db(msg.topic, msg.payload)


def on_subscribe(*args):
    print(u"[%s]Subscribe ok!" % datetime.datetime.now())
    print args


client = mqtt.Client(
    client_id="test180209",  # 用来标识设备的ID，用户可自己定义，在同一个实例下，每个实体设备需要有一个唯一的ID
)

client.username_pw_set(user, pwd)  # 设置用户名，密码
client.on_connect = on_connect  # 连接成功的回调
client.on_disconnect = on_disconnect  # 断线的回调
client.on_message = on_message  # 接受消息的操作
client.on_subscribe = on_subscribe

while True:
    try:
        print "[%s]Try to connect server..." % datetime.datetime.now()
        client.connect(endpoint, port, 60)  # 连接服务 keepalive=60
        client.loop_forever()
        print "[%s]Loop end！" % datetime.datetime.now()
    except Exception as e:
        print "[%s]MQTT exception: %s" % (datetime.datetime.now(), str(e))
        print "[%s]Will try again ..." % datetime.datetime.now()
        time.sleep(5)
