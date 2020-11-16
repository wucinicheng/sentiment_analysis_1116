#基于百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
    # coding=utf-8
    
import http.client
import hashlib
import urllib
import random
import json


CONFIG={
    "appid":"20200829000554761",# 填写你的appid
    "secretKey":"U6siBpQpiQSwVS9pHNJI",# 填写你的密钥
    "myurl":"/api/trans/vip/translate"

}

########################################################
#                                                      #
# 内部appid与secretKey来自个人申请API，可根据个人情况进行修改 #
#                                                      #
######################################################## 
class translate_baidu(object):
    def __init__(self, config=CONFIG):
           super(translate_baidu, self).__init__()
           self.config = config

    def translate(self, text, source="yue", target="zh"):
    
        httpClient = None
        salt = random.randint(32768, 65536)
        q = text
        sign = self.config['appid'] + q + str(salt) + self.config['secretKey']
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = self.config['myurl'] + '?appid=' + self.config['appid'] + '&q=' + urllib.parse.quote(q) + '&from=' + source + '&to=' + target + '&salt=' + str(
        salt) + '&sign=' + sign
    
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
    
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            if httpClient:
                httpClient.close()
        except Exception as e:
            print(e)
        if "trans_result" in result:
            return result['trans_result'][0]['dst']
        else:
            return "error"

if __name__ == '__main__':
    translate = translate_baidu()
    print(translate.translate('佢一啲都唔中意呢种感觉，因为佢会畀人喺安逸中沉沦。'))
        