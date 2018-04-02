# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import urllib
from urllib import urlencode

App_key = "50d53e7b519f6b5ca65ca214b1e8948a"


# ----------------------------------
# 股票数据调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/21
# ----------------------------------
def main():
    # 配置您申请的APPKey
    appkey = "50d53e7b519f6b5ca65ca214b1e8948a"

    # 1.沪深股市
    request_sh(appkey, "GET")


# 沪深股市
def request_sh(gid, app_key=App_key, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/hs"
    params = {
        "gid": gid,  # 股票编号，上海股市以sh开头，深圳股市以sz开头如：sh601009
        "key": app_key,  # APP Key

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print res["result"][0]
            data = "\n股票名称:" + res["result"][0]["data"]['name'] + "\n" +\
                "股票编号:" + res["result"][0]["data"]['gid'] + "\n" + \
                "当前价格:" + res["result"][0]["data"]['nowPri'] + "\n" + \
                "涨跌百分比:" + res["result"][0]["data"]['increPer'] + "\n" +\
                "涨跌额:" + res["result"][0]["data"]['increase'] + "\n" + \
                "今日最高价:" + res["result"][0]["data"]['todayMax'] + "\n" + \
                "今日最低价:" + res["result"][0]["data"]['todayMin'] + "\n" + \
                "成交量:" + res["result"][0]["data"]['traNumber'] + "\n" + \
                "成交金额:" + res["result"][0]["data"]['traAmount'] + "\n" + \
                "今日开盘价:" + res["result"][0]["data"]['todayStartPri'] + "\n" +\
                "昨日收盘价:" + res["result"][0]["data"]['yestodEndPri'] + "\n" +\
                "数据时间:" + res["result"][0]["data"]['date'] + " " + res["result"][0]["data"]['time'] + "\n"

            return data
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"

    return None


if __name__ == '__main__':
    request_sh(app_key=App_key, gid='sh601009')
