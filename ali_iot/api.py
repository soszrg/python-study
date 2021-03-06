# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import json
from ali_iot.client_util import ClientUtil
from ali_iot.service_util import ServiceUtil
from aliyunsdkiot.request.v20170420 import CreateProductRequest
from aliyunsdkiot.request.v20170420 import UpdateProductRequest
from aliyunsdkiot.request.v20170420 import RegistDeviceRequest
from aliyunsdkiot.request.v20170420 import ApplyDeviceWithNamesRequest
from aliyunsdkiot.request.v20170420 import QueryApplyStatusRequest
from aliyunsdkiot.request.v20170420 import BatchGetDeviceStateRequest
from aliyunsdkiot.request.v20170420 import QueryDeviceByNameRequest
from aliyunsdkiot.request.v20170420 import QueryDeviceRequest
from aliyunsdkiot.request.v20170420 import QueryPageByApplyIdRequest
from aliyunsdkiot.request.v20170420 import PubRequest
from aliyunsdkiot.request.v20170420 import PubBroadcastRequest
from aliyunsdkiot.request.v20170420 import RRpcRequest
from aliyunsdkiot.request.v20170420 import GetDeviceShadowRequest
from aliyunsdkiot.request.v20170420 import UpdateDeviceShadowRequest


class Test:
    clt = ClientUtil.create_client()

    def __init__(self):
        pass

    def createProductTest(self):
        request = CreateProductRequest.CreateProductRequest()
        productName = ServiceUtil.product_name_generator()
        print (productName)
        desc = 'iot python sdk create'
        request.set_Name(productName)
        request.set_Desc(desc)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            product_info = result_json['ProductInfo']
            print (product_info)
            return product_info['ProductKey']
        else:
            print('失败')

    def updateProductTest(self, productKey):
        request = UpdateProductRequest.UpdateProductRequest()
        request.set_ProductKey(productKey)
        request.set_ProductName('name_zrgtest')
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('updateProduct success')
        else:
            print ('updateProduct failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def registDeviceTest(self, productKey, deviceName):
        request = RegistDeviceRequest.RegistDeviceRequest()
        request.set_accept_format('json')
        request.set_DeviceName(deviceName)
        request.set_ProductKey(productKey)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('registDevice success')
        else:
            print ('registDevice failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def applyDeviceWithNamesTest(self, productKey, deviceNames):
        request = ApplyDeviceWithNamesRequest.ApplyDeviceWithNamesRequest()
        request.set_ProductKey(productKey)
        request.set_DeviceNames(deviceNames)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('applyDeviceWithNames success')
            return result_json['ApplyId']
        else:
            print (
            'applyDeviceWithNames failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def queryApplyStatusTest(self, applyId):
        request = QueryApplyStatusRequest.QueryApplyStatusRequest()
        request.set_ApplyId(applyId)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('queryApplyStatus success ', result)
        else:
            print (
            'applyDeviceWithNames failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def queryPageByApplyIdTest(self, applyId):
        request = QueryPageByApplyIdRequest.QueryPageByApplyIdRequest()
        request.set_ApplyId(applyId)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('queryPageByApplyId success ', result)
        else:
            print (
            'queryPageByApplyId failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def queryDeviceByNameTest(self, productKey, deviceName):
        request = QueryDeviceByNameRequest.QueryDeviceByNameRequest()
        request.set_ProductKey(productKey)
        request.set_DeviceName(deviceName)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('queryDeviceByName success ', result)
        else:
            print (
            'queryDeviceByName failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def queryDeviceTest(self, productKey):
        request = QueryDeviceRequest.QueryDeviceRequest()
        request.set_ProductKey(productKey)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('queryDevice success ', result)
        else:
            print ('queryDevice failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def batchGetDeviceStatusTest(self, productKey, deviceNames):
        request = BatchGetDeviceStateRequest.BatchGetDeviceStateRequest()
        request.set_ProductKey(productKey)
        request.set_DeviceNames(deviceNames)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('queryDevice success ', result)
        else:
            print ('queryDevice failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def getDeviceShadowTest(self, productKey, deviceName):
        request = GetDeviceShadowRequest.GetDeviceShadowRequest()
        request.set_ProductKey(productKey)
        request.set_DeviceName(deviceName)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('getDeviceShadow success', result)
        else:
            print (
            'getDeviceShadow failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def updateDeviceShadowTest(self, productKey, deviceName):
        request = UpdateDeviceShadowRequest.UpdateDeviceShadowRequest()
        request.set_ProductKey(productKey)
        request.set_DeviceName(deviceName)
        request.set_ShadowMessage(
            '{"method":"update","state":{"desired":{"window":"open","temperature":25},"reported":{"id":"3333"}},"version":1}')
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('updateDeviceShadow success ')
        else:
            print (
            'updateDeviceShadow failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def pubTest(self, productKey, deviceName):
        request = PubRequest.PubRequest()
        request.set_ProductKey(productKey)
        # message = 'e2FhYWFhfXtiYmJiYn0='
        message = base64.b64encode(json.dumps({"a": 1}))
        topic = '/' + productKey + '/' + deviceName + '/status'
        request.set_TopicFullName(topic)
        request.set_MessageContent(message)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('pub success ')
        else:
            print (
            'pub failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json['RequestId'])

    def pubBroadcastTest(self, productKey):
        request = PubBroadcastRequest.PubBroadcastRequest()
        request.set_ProductKey(productKey)
        request.set_TopicFullName('/broadcast/' + productKey + '/test')
        request.set_MessageContent('e2FhYWFhfXtiYmJiYn0=')
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('pubBroadcast success ')
        else:
            print ('pubBroadcast failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json[
                'RequestId'])

    def rrpcTest(self, productKey, deviceName):
        request = RRpcRequest.RRpcRequest()
        request.set_ProductKey(productKey)
        request.set_DeviceName(deviceName)
        request.set_RequestBase64Byte('e2FhYWFhfXtiYmJiYn0=')
        request.set_Timeout(5000)
        result = self.clt.do_action_with_exception(request)
        result_json = json.JSONDecoder().decode(result)
        if result_json['Success']:
            print('rrpc success ', result)
        else:
            print (
                'rrpc failed , errorMessage=' + result_json['ErrorMessage'] + ', requestId=' + result_json['RequestId'])


if __name__ == '__main__':
    test = Test()
    productKey = 'W3QlVga3u7q'
    # productKey = 'oWFr7m8x51Q'
    # productKey = test.createProductTest()
    # test.updateProductTest(productKey)
    # deviceNames = ServiceUtil.device_name_generator(6)
    test.registDeviceTest(productKey, "zrgtest122201")
    # applyId = test.applyDeviceWithNamesTest(productKey, deviceNames)
    # test.queryApplyStatusTest(applyId)
    # test.queryPageByApplyIdTest(applyId)
    # test.queryDeviceByNameTest(productKey, deviceNames[0])
    # test.queryDeviceTest(productKey)
    # test.batchGetDeviceStatusTest(productKey, deviceNames)
    # test.updateDeviceShadowTest(productKey, deviceNames[0])
    # test.getDeviceShadowTest(productKey, deviceNames[0])
    # test.pubTest('oWFr7m8x51Q', 'zrgtest121101')
    test.pubBroadcastTest(productKey)
    # test.rrpcTest(productKey, deviceNames[0])
