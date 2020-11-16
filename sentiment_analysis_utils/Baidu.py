# -*- coding: utf-8 -*-
# @Time    : 2020/9/24 20:38
# @Author  : CHAO
# @File    : Baidu.py
# @Software: PyCharm

import requests
import json

class baiduSentimentAnalysis:

    DEFAULT_AK = 'Uh3eqy7yCry5oNMYNqmoKvNg' # 百度AI中的
    DEFAULT_SK = 'RCmNQPQrB3m1ayDUhquUfPgjuwCsLNFd'

    def __init__(self, ak=DEFAULT_AK, sk=DEFAULT_SK):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(ak, sk)
        res = requests.post(host)
        r = json.loads(res.text)
        self.token = r["access_token"]


    def get_sentiment(self, text):

        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify_custom?charset=UTF-8&access_token={}'.format(self.token)
        data = {
            'text':text
        }
        data = json.dumps(data)
        try:
            res = requests.post(url,data=data).text
            sentiment = json.loads(res)["items"][0]["sentiment"]  # 在这里对百度API的返回结果做了简化处理，进取出其sentiment项
        except:
            sentiment = "情感值获取出错"

        return str(sentiment)

if __name__ == "__main__":
    # 首先实例化一个百度情感分析对象
    baiduSA = baiduSentimentAnalysis()
    # 调用对象中的get_sentiment方法获取
    text = "香港废青穿黑衣哭口号，现场没有人回应，可怜呐。终是曲子终曱散，狗薪水无处觅，蟑螂下尽一场梦[躺手]"
    sentiment = baiduSA.get_sentiment(text)
    print("%s:%s" % (sentiment, text))

