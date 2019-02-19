# -*- encoding: utf-8 -*-
import logging

import time
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest

log = logging.getLogger('view')


if __name__ == '__main__':
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
    alipay_client_config.app_id = '2017020805562382'
    alipay_client_config.app_private_key = 'MIIEowIBAAKCAQEApSLuzkBrcuivMbmy/qaaYRBzKsZ24ALQMx580rT5BBLHiRcnRYcr4kz90wuE+akLfY9AYztMrGVZ6bQsnkkwH303sPUTB0wffN9By4FT/cvxMGsMYguL4zmLyUGl1C2YhuwvP1WYq08tuzRSMe5CaOFhxGrqnfDV1C6z7oowU/gugDjHUfgL+N9cohbXj5chKRcUOtZB0kSO0kn+AxULroc4hO1MEE4B/HQy1wNRX2Yjsh1IFw8Es32JIT60nAzOyR2MQcMdxZV4BiQS4DUB0x5Z55D2hTERliB95WPkhlNdq4BlQmKN/vAChi0zyKNnBkiOwV7u+pnwM4L4U4M3IwIDAQABAoIBACcoJWAavl+89O3hjqP7dVfWwrg93yo3AI9eh1KfPvzMRywmpVVDPBCpGPbWIG3iu6rGMQpWoVOvpKZZ5sqRqCuPUYlQU3bDgiPl/H/45qWjmklU2NbWzhDPMGpEesHZHfXAQ2PNNCpK2Bkvyt20FWMxLjGY+JEC7nElsdy6P8NpEGgWCWWvx4lhZ+anrSHiu+c/wp8ujsZSGILqiF36InCqV0lW64x/qtiSmJ4knBNbm1vMAXODD9Rw/fw7pWo/h4kPA8+vApSaBhTUKsgJ+93UoFr0h2FuJDXYrr+uVncjIFgQIMUOavS6DlQbKZ6IciIcRv7U0dE4mggiv0C9u0ECgYEA1eFPepCpiBz4IXYW1kmmce3WbzVKDsvWKeLOlc8rXtWkBmjbQEayRo8X8Hfthd8brvEnQUPLAuBRcc7LQpFThx6NVfmCrA1ofEHMS2P5DSOtpVHqhgmmEbInpj+/QH8DAs3O6vzTG2HDKqNJAx7drrBnF1+if4/7HV9pGPaBbysCgYEAxag6ZDfU2o6X8GFyiHaBsFGphI2ZrOpYiVvDLYxeK3ND7frjpEbi+Y/Mp9YzvYg0ErZtq6KgiKc1A0UdB9rNi8qcptn2vKXY26EeQoHBuR6peG4Ic63ce+dzIfhSofYntOQkpb4YPpJJMYh1qBoWoKMiniR1D5KDOeAUvikym+kCgYBxAIP/m+MWmUe4Vi4mte8NDr5XL26bdrMGmmDP4g9mIbZx9ICy6ydSBFR/pr2GF6UGvz8gSnM+Z8pgOQRHfYUGROwj2pph0Qu9av5HbuCtQoaCbE9e1kY530j3m4KuzuyGVLrYiQ/4zaRSKMdwsKQroeQ2Az9V6nqgwEJFACjO1QKBgFhLmioCttcbM8xx+5PyPGTjVfKcvrV7yikyELJcLgUC7Kl2lhJgiCwrjKS9D0fvfDOPwtYVQ9lHuGrJiPplR8TWsbvnSk1jWMhj5PyYsk1b4SCnJqdmV0QSVGAsad1n9Lzd3XEcxf/NoVy7NLPvU4RW27QBXTmjnXNRInMAPFdhAoGBAIMo+q4v8G2a9u3CzGHPFbKHBupuhQgCs4gLSKx2uo0mI+Hc8PNHWuSodCQW7zWknj4xuUSkzYVv7drOVUOj8DXB5C+kYKqPyXZ4MOqyFTkrqDdrMap+ikOpW/pxxteEqFl+08yJmLvrnvU8kRmnV8HMxg17RGlIy33iNPk3aTg0'
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0g+wU7BfTgUQPqju7O6pGt2bnFQljOMEayQ51drgcZdJNhoN8A/00Fd0u7hYs/xD46kXzs0PeDPx9noaxJgphBq5pvJPWGfRNXTd83D3Y0HFBVKDCBLH3SDPFQfJMNA/jPfMCZ4R3IP6SR3zAPzXKkHnPyX3h7+ZVFkXjhZIgVbeQ2rd8CZiQNYGouMA12fFIxlEY3bBTayiXPihsavSTN33mj8RdH3vOF52XGpQv7MXR56nAkoAvjlg9hyZa9Un00/xGhnJNMmUYQDG1aCmeVkcpCD1PBlzMuJjjPn7rDeRlkzINPIMBIaOhfdkK6bWjjIIEj0k3JMLWSl/fkMWTwIDAQAB'

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=log)

    """
    构造唤起支付宝客户端支付时传递的请求串示例：alipay.trade.app.pay
    """
    model = AlipayTradeAppPayModel()
    model.timeout_express = "90m"
    model.total_amount = "0.01"
    model.seller_id = "2088102169162785"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = "product_des"
    model.subject = "iphone"
    model.out_trade_no = "%d" % 1546067572847
    request = AlipayTradeAppPayRequest(biz_model=model)
    response = client.sdk_execute(request)
    # log.info("alipay.trade.app.pay response:" + response)
    print("alipay.trade.app.pay response:" + response)
