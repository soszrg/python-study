# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
from threading import Thread

import paho.mqtt.client as mqtt

username = '44a9c0e21b4211e7a554fa163e876164/d3ffeca4259611e7a554fa163e876164'
password = '8DMayouGrZNK68s2DWypIc/GEnA9vpEiy8wvJobjvGE='
topic = '44a9c0e21b4211e7a554fa163e876164/0f72d67e1b7511e7a554fa163e876164/d3ffeca4259611e7a554fa163e876164/status/json'
clientid = 'd3ffeca4259611e7a554fa163e876164'
host = '44a9c0e21b4211e7a554fa163e876164.mqtt.iot.gz.baidubce.com'
port = 1883


class MqttManager(object):
    def __init__(self, username, password, clientid):
        self.is_connected = False
        self.client = mqtt.Client(clientid)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publisher

    def connect(self):
        print "Try to connect server..."
        self.client.connect(host, port)
        self.client.loop_start()
        while not self.is_connected:
            print "Wait connect done..."
            time.sleep(1)
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
    mqtt_client.subscribe(topic)

    i = 0
    while True:
        mqtt_client.publisher(topic, "test%s" % i)
        i += 1
        # if i == 10:
        #     mqtt_client.disconnect()
        time.sleep(1)
    # if mqtt_client.is_connected:
    #     mqtt_client.disconnect()
    #     while mqtt_client.is_connected:
    #         print "Wait disconnect done..."
    #         time.sleep(1)
    #     print "===disconnect==="
    while True:
        time.sleep(1)
except Exception, e:
    print u"错误:{0} ".format(str(e))

