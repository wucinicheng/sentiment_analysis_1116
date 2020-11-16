#!/usr/bin/env python 
# -*- coding:utf-8 -*-

#
# 机器翻译2.0(niutrans) WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 1.接口文档（必看）：https://www.xfyun.cn/doc/nlp/niutrans/API.html
# 2.错误码链接：https://www.xfyun.cn/document/error-code （错误码code为5位数字）
# 3.个性化翻译术语自定义：
#   登陆开放平台 https://www.xfyun.cn/
#   在控制台--机器翻译(niutrans)--自定义翻译处
#   上传自定义翻译文件（打开上传或更新窗口，可下载示例文件）
#

import requests
import datetime
import hashlib
import base64
import hmac
import json

CONFIG = {
    "APPID":"5f4cb1fb",# 应用ID（到控制台获取）
    "APIKey":"e37c33a6800b095fcdd3466e6c50ad07",# 接口APIKey（到控制台机器翻译服务页面获取）
    "Secret":"bae369baf297d237d77ace3248926c94",# 接口APISercet（到控制台机器翻译服务页面获取）
    "RequestUri":"/v2/ots",
    "Host":"ntrans.xfyun.cn",
    "requestMethod":"POST",
    "signMethod":"hmac-sha256",
    "HttpProto":"HTTP/1.1"
}

class translate_xunfei(object):
    def __init__(self,config=CONFIG):
        self.config = config
        # 设置url
        # print(host)
        self.config['url']="https://"+self.config['Host']+self.config['RequestUri']

    def translate(self, text="你好", source="yue", target="zh"):
        self.set_self(text,source,target)
        return self.call_url()


    def set_self(self, text, source, target):
        # 设置当前时间
        curTime_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        self.Text = text
        self.BusinessArgs={
        "from":source,
        "to":target
        }
        return self

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.config['Host'] + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.config['requestMethod'] + " " + self.config['RequestUri'] \
                        + " " + self.config['HttpProto'] + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.config['Secret'].encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        #print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.config['APIKey'], self.config['signMethod'], sign)
        #print(authHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.config['Host'],
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        content = str(base64.b64encode(self.Text.encode('utf-8')), 'utf-8')
        postdata = {
            "common": {"app_id": self.config['APPID']},
            "business": self.BusinessArgs,
            "data": {
                "text": content,
            }
        }
        body = json.dumps(postdata)
        #print(body)
        return body

    def call_url(self):
        if self.config['APPID'] == '' or self.config['APIKey'] == '' or self.config['Secret'] == '':
            print('Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。')
        else:
            code = 0
            body=self.get_body()
            headers=self.init_header(body)
            #print(self.url)
            response = requests.post(self.config['url'], data=body, headers=headers,timeout=8)
            status_code = response.status_code
            #print(response.content)
            if status_code!=200:
                # 鉴权失败
                print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/nlp/niutrans/API.html")
            else:
                # 鉴权成功
                respData = json.loads(response.text)
                return respData['data']['result']['trans_result']['dst']
                # 以下仅用于调试
                code = str(respData["code"])
                if code!='0':
                    print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")

if __name__ == '__main__':
    ##示例:  host="ntrans.xfyun.cn"域名形式
    host = "ntrans.xfyun.cn"
    #初始化类
    text = "佢一啲都唔中意呢种感觉，因为佢会畀人喺安逸中沉沦。"
    gClass=translate_xunfei()
    print(gClass.translate(text))
