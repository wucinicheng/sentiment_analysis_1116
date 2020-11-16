import binascii
import hashlib
import hmac
import sys
import json
import requests
import urllib.parse
import time
import random

CONFIG = {
    "SecretId":"AKIDzlKaZE5TzED4vVPyrSlsjpfFY4RZRp22",# 用户必须准备好的secretId和secretKey,可以在 https://console.cloud.tencent.com/capi 获取
    "secretKey":"sUpyrSnrgEZfW6PRCixua09KEsVtxkHf",
    "actionData":"TextTranslate",# Action一般是操作名称
    "uriData":"tmt.tencentcloudapi.com",# 
    "signMethod":"HmacSHA256",
    "region":"ap-hongkong",
    "requestMethod":"GET",
    "versionData":"2018-03-21",
}



# 在此处定义一些必须的内容
timeData = str(int(time.time())) # 时间戳
nonceData = int(random.random()*10000) # Nonce，官网给的信息：随机正整数，与 Timestamp 联合起来， 用于防止重放攻击

def dictToStr(dictData):
    '''
    本方法主要是将Dict转为List并且拼接成字符串
    :param dictData:
    :return: 拼接好的字符串
    '''
    tempList = []
    for eveKey, eveValue in dictData.items():
        tempList.append(str(eveKey) + "=" + str(eveValue))
    return "&".join(tempList)

class translate_tencent(object):
    """docstring for translate_tencent"""
    def __init__(self, CONFIG=CONFIG):
        super(translate_tencent, self).__init__()
        self.config = CONFIG
        # 根据参数中的signMethod来选择加密方式
        if self.config['signMethod'] == 'HmacSHA256':
            self.config['digestmod'] = hashlib.sha256
        elif self.config['signMethod'] == 'HmacSHA1':
            self.config['digestmod'] = hashlib.sha1

    def sign(self, signStr):
        '''
        该方法主要是实现腾讯云的签名功能
        :param secretKey: 用户的secretKey
        :param signStr: 传递进来字符串，加密时需要使用
        :param signMethod: 加密方法
        :return:
        '''
        if sys.version_info[0] > 2:
            signStr = signStr.encode("utf-8")
            secretKey = self.config['secretKey'].encode("utf-8")
        # 完成加密，生成加密后的数据
        hashed = hmac.new(secretKey, signStr, self.config['digestmod'])
        base64 = binascii.b2a_base64(hashed.digest())[:-1]

        if sys.version_info[0] > 2:
            base64 = base64.decode()

        return base64


    def translate(self, text, source="zh",target="en"):
        if source==target:
            if source=="en":
                return text
            else:
                return self.translate(self.translate(text,source,'en'),"en",target)
        # 签名时需要的字典
        # 首先对所有请求参数按参数名做字典序升序排列，所谓字典序升序排列，
        # 直观上就如同在字典中排列单词一样排序，按照字母表或数字表里递增
        # 顺序的排列次序，即先考虑第一个“字母”，在相同的情况下考虑第二
        # 个“字母”，依此类推。
        signDictData = {
            'Action' : self.config['actionData'],
            'Nonce' : int(random.random()*10000),
            'ProjectId':0,
            'Region' : self.config['region'],
            'SecretId' : self.config['SecretId'],
            'SignatureMethod':self.config['signMethod'],
            'Source': source,
            'SourceText': text,
            'Target': target,
            'Timestamp' : int(str(int(time.time()))),
            'Version': self.config['versionData'] ,
        }
        # request方法生成URI的后缀
        requestStr = "%s%s%s%s%s"%(self.config['requestMethod'],self.config['uriData'],"/","?",dictToStr(signDictData))
        # 调用签名方法，同时将结果进行url编码，官方文档描述如下：
        # 生成的签名串并不能直接作为请求参数，需要对其进行 URL 编码。 注意：如果用户的请求方法是GET，则对所有请求参
        # 数值均需要做URL编码。 如上一步生成的签名串为 EliP9YW3pW28FpsEdkXt/+WcGeI= ，最终得到的签名串请求参数(Signature)
        # 为： EliP9YW3pW28FpsEdkXt%2f%2bWcGeI%3d ，它将用于生成最终的请求URL。
        signDictData["Signature"] = urllib.parse.quote(self.sign(requestStr))
        # 根据uri构建请求的url
        requestUrl = "https://%s/?"%(self.config['uriData'])
        # 将请求的url和参数进行拼接
        requestUrlWithArgs = requestUrl + dictToStr(signDictData)
        # requestUrlWithArgs=requestUrlWithArgs.encode('utf8').decode()
        # 获得response
        responseData = requests.get(requestUrlWithArgs).content.decode('utf8') # urllib.request.urlopen(requestUrlWithArgs).read().decode("utf-8")


        # 获得到的结果形式：
        #  {"Response":{"RequestId":"0fd2e5b4-0beb-4e01-906f-e63dd7dd33af","Source":"en","Target":"zh","TargetText":"\u4f60\u597d\u4e16\u754c"}}
        return json.loads(responseData)["Response"]["TargetText"]

if __name__ == '__main__':
    text = "佢一啲都唔中意呢种感觉，因为佢会畀人喺安逸中沉沦。"
    trans = translate_tencent()
    out=trans.translate(text,"zh","zh")
    print(out)