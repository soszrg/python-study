# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import random
import time
from threading import Thread

import paho.mqtt.client as mqtt

# username = '81579cea3a1811e7a554fa163e876164/83e134fa42bd11e7a554fa163e876164'
# password = '5BNr3VgYOCznK0hFcFJogDD7HLJs1pilXrv2s6CV9Js='
# topic = '81579cea3a1811e7a554fa163e876164/9c0fa1043a1811e7a554fa163e876164/83e134fa42bd11e7a554fa163e876164/status/json'
# clientid = '83e134fa42bd11e7a554fa163e876164'
# host = '81579cea3a1811e7a554fa163e876164.mqtt.iot.gz.baidubce.com'
# port = 1883

username = 'ebf99816-ce8b-11e7-86c3-00163e105361'
password = '123456'
topic = 'd2c/ebf99816-ce8b-11e7-86c3-00163e105361/status'
clientid = 'ebf99816-ce8b-11e7-86c3-00163e105361'
host = 'v2test.fogcloud.io'
port = 18832

# username = '81579cea3a1811e7a554fa163e876164/83e134fa42bd11e7a554fa163e876164'
# password = '5BNr3VgYOCznK0hFcFJogDD7HLJs1pilXrv2s6CV9Js='
# topic = '81579cea3a1811e7a554fa163e876164/9c0fa1043a1811e7a554fa163e876164/83e134fa42bd11e7a554fa163e876164/status/json'
# clientid = '83e134fa42bd11e7a554fa163e876164'
# host = '81579cea3a1811e7a554fa163e876164.mqtt.iot.gz.baidubce.com'
# port = 1883
#


class MqttManager(object):
    def __init__(self, username, password, clientid):
        self.is_connected = False
        self.is_loop = False
        self.client = mqtt.Client(clientid)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publisher

    def connect(self):
        print "Try to connect server..."
        # print "connect return code: %d" % self.client.connect(host, port)
        # print "Wait connect done..."
        self.is_loop = True
        self.client.loop_start()
        while not self.is_connected:
            try:
                print "connect return code: %d" % self.client.connect(host, port)
                if self.client._thread:
                    self.client.loop_start()
            except Exception as e:
                print "connect error: %s" % e.strerror
            print "Wait connect done..."
            time.sleep(5)
        print "Connect Done"

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, topic_name):
        print "Try to subscribe[%s]" % topic_name
        self.client.subscribe(str(topic_name))

    def publisher(self, topic_name, message):
        self.client.publish(topic_name, message)

    def unsubscribe(self, topic_name):
        self.client.unsubscribe(str(topic_name))

    # 连接成功后
    def _on_connect(self, client, userdata, flags, rc):
        self.is_connected = True
        print(u"[INFO] 连接MQTT服务器:返回码 " + str(rc))

    def _on_disconnect(self, client, userdata, rc):
        self.is_connected = False
        # self.client.loop_stop()
        self.connect()
        print(u"[INFO] 断开MQTT服务器:返回码 " + str(rc))

    # 接受发布消息.
    def _on_message(self, client, userdata, msg):
        print(u"[INFO] 在 %s 接收到来自 %s 通道的消息,内容为: %s" % (
            time.asctime(time.localtime(time.time())), msg.topic, str(msg.payload)))

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print(u"[INFO] 订阅成功!")
        print userdata, granted_qos

    def _on_publisher(self, client, userdata, mid):
        print(u"[INFO] 发布成功:%s" % mid)


try:
    mqtt_client = MqttManager(username, password, clientid)
    mqtt_client.connect()

    # while True:
    #     rand_num = random.randint(0, 50)
    #     payload = {
    #         "DeviceMode": 1,
    #         "PM2_5": rand_num,
    #         "PM2_5Avg": 12,
    #         "CO2": 0,
    #         "Temperature": 0,
    #         "Humidity": 0,
    #         "Pressure": 12,
    #         "SensorStamp": 99,
    #         "MotorRPM": 99,
    #         "FilterSta": 99,
    #         "OperHours": 99,
    #         "ErrorCode": 1,
    #         "MsgType": 5
    #     }
    #     # print json.dumps(payload) % (random.randint(1, 10))
    #     mqtt_client.publisher(topic, json.dumps(payload))
    #     time.sleep(5)
    # try:
    #     mqtt_client.client.loop_forever()
    # except Exception:
    #     mqtt_client.connect()
    # while True:
    #     print "===>sleep 3 secs"
    #     time.sleep(3)
except Exception, e:
    print u"错误:{0} ".format(str(e))

