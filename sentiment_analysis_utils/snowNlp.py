# -*- coding: utf-8 -*-
# @Time    : 2020/9/27 16:09
# @Author  : CHAO
# @File    : snowNlp.py
# @Software: PyCharm
from snownlp import sentiment


class snownlpSentimentAnalysis:

    NEG_SENTS_PATH = 'data/sents/neg_sents.txt'  # 存放负向情感文本
    POS_SENTS_PATH = 'data/sents/pos_sents.txt'  # 存放正向情感文本

    def __init__(self, neg_sents_path=NEG_SENTS_PATH, pos_sents_path=POS_SENTS_PATH):
        sentiment.train(neg_sents_path, pos_sents_path)


    def get_sentiment(self, text):
        sent = sentiment.classify(text)
        return sent


if __name__ == '__main__':
    sSA = snownlpSentimentAnalysis()
    text = "有一件事就不能说的例如光复香港时代革命五大诉求空缺一不可我就不buy的"
    sent = sSA.get_sentiment(text)
    if sent < 0.4:
        print("这句话是港独！")
    else:
        print("这句话不是港独！")
