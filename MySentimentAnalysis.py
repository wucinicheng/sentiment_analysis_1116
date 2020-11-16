# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 12:44
# @Author  : CHAO
# @File    : MySentimentAnalysis.py
# @Software: PyCharm
import time

from sentiment_analysis_utils.Baidu import baiduSentimentAnalysis
from sentiment_analysis_utils.HarvestText import harvesttextSentimentAnalysis
from sentiment_analysis_utils.snowNlp import snownlpSentimentAnalysis
from translate_API import baidu


class MySentimentAnalysis:
    DEFAULT_AK = 'Uh3eqy7yCry5oNMYNqmoKvNg'             # 百度情感分析AI中的
    DEFAULT_SK = 'RCmNQPQrB3m1ayDUhquUfPgjuwCsLNFd'     # 百度情感分析AI中的


    NEG_SENTS_PATH = 'sentiment_analysis_utils/data/sents/neg_sents.txt'  # 存放负向情感文本
    POS_SENTS_PATH = 'sentiment_analysis_utils/data/sents/pos_sents.txt'  # 存放正向情感文本

    NEG_SEEDS_PATH = 'sentiment_analysis_utils/data/seeds/neg_seeds.txt'  # 存放负向情感种子词
    POS_SEEDS_PATH = 'sentiment_analysis_utils/data/seeds/pos_seeds.txt'  # 存放正向情感种子词

    def __init__(self):
        self.trans = baidu.translate_baidu() # 用百度速度很快
        self.baiduSA = baiduSentimentAnalysis(self.DEFAULT_AK, self.DEFAULT_SK)
        self.htSA = harvesttextSentimentAnalysis(self.NEG_SENTS_PATH, self.POS_SENTS_PATH, self.NEG_SEEDS_PATH, self.POS_SEEDS_PATH)
        self.snSA = snownlpSentimentAnalysis(self.NEG_SENTS_PATH, self.POS_SENTS_PATH)

    def get_sentiment(self, text):
        trans_text = text
        trans_text = self.trans.translate(text)
        baiduSent = self.baiduSA.get_sentiment(trans_text)
        htSent = self.htSA.get_sentiment(trans_text)
        snSent = self.snSA.get_sentiment(trans_text)
        time.sleep(1)  # 百度API的QPS限制

        res = {
            "baiduSentiment": baiduSent,    #该方法返回参数0表示neg，1标志mid， 2表示pos
            "harvesttextSentiment": htSent, #该方法返回参数小于0表示neg，大于0表示pos
            "snownlpSentiment": snSent      #该方法返回参数小于0.4表示neg，大于0.4表示pos，但不绝对，只是推荐
        }

        return res

if __name__ == "__main__":
    print("载入模型......")
    mySent = MySentimentAnalysis()
    print("开始预测......")
    text1 = "香港废青穿黑衣哭口号，现场没有人回应，可怜呐。终是曲子终曱散，狗薪水无处觅，蟑螂下尽一场梦[躺手]"
    text2 = "我相信姐也是這麼走來的 我有一天也會的 一起跟著姐混囉！ 打倒中共共殘襠 消滅中共共慘襠 光復香港時代革命 為我 #爆料革命 必勝"
    text3 = "有一件事就不能说的例如光复香港时代革命五大诉求空缺一不可我就不buy的"
    print(text1 + "\n" + mySent.get_sentiment(text1).__str__())
    print(text2 + "\n" + mySent.get_sentiment(text2).__str__())
    print(text3 + "\n" + mySent.get_sentiment(text3).__str__())