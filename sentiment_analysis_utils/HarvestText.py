# -*- coding: utf-8 -*-
# @Time    : 2020/9/24 20:38
# @Author  : CHAO
# @File    : HarvestText.py
# @Software: PyCharm
from harvesttext import HarvestText

class harvesttextSentimentAnalysis:

    NEG_SENTS_PATH = 'data/sents/neg_sents.txt'  # 存放负向情感文本
    POS_SENTS_PATH = 'data/sents/pos_sents.txt'  # 存放正向情感文本
    NEG_SEEDS_PATH = 'data/seeds/neg_seeds.txt'  # 存放负向情感种子词
    POS_SEEDS_PATH = 'data/seeds/pos_seeds.txt'  # 存放正向情感种子词

    # 初始化函数，生成ht对象，并用已存在的字典进行训练
    def __init__(self, neg_sents_path=NEG_SENTS_PATH, pos_sents_path=POS_SENTS_PATH, neg_seeds_path=NEG_SEEDS_PATH, pos_seeds_path=POS_SEEDS_PATH):
        self.ht = HarvestText()
        self.train_ht(neg_sents_path, pos_sents_path, neg_seeds_path, pos_seeds_path)


    # 读取正负情感例句
    def read_sents(self, sent_path):
        sents = []
        with open(sent_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = line.replace('\n', '')  # 出去换行符
                sents.append(line)
                line = f.readline()
        return sents

    # 读取种子词
    def read_seeds(self, seeds_path):
        seeds = []
        with open(seeds_path, 'r', encoding='UTF-8') as f:
            line = f.readline()
            while line:
                line = line.replace('\n', '')
                seeds.append(line)
                line = f.readline()
        return seeds


    # 训练对象中的ht模型
    def train_ht(self, neg_sents_path, pos_sents_path, neg_seeds_path, pos_seeds_path):
        neg_sents = self.read_sents(neg_sents_path)
        pos_sents = self.read_sents(pos_sents_path)
        sents = []
        sents.extend(neg_sents)
        sents.extend(pos_sents)

        pos_seeds = self.read_seeds(pos_seeds_path)

        neg_seeds = self.read_seeds(neg_seeds_path)

        self.ht.build_sent_dict(sents, min_times=3, scale="+-1", pos_seeds=pos_seeds, neg_seeds=neg_seeds) # 支持自定义，具体看build_sent_dict函数说明文档

    # 预测种子词汇的情感值
    def get_sentiment(self, sent):
        emotion_value = self.ht.analyse_sent(sent)
        return emotion_value


if __name__ == "__main__":
    hsa = harvesttextSentimentAnalysis()
    text = "废青真的是到处认爹，一门心思做别人的狗，你就是到美国的领事馆就能出得了境？"
    print("%f:%s" % (hsa.get_sentiment(text), text))
