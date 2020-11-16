# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 10:13
# @Author  : CHAO
# @File    : __init__.py.py
# @Software: PyCharm
from MySentimentAnalysis import MySentimentAnalysis

if __name__ == "__main__":
    mySent = MySentimentAnalysis()
    text1 = "香港废青穿黑衣哭口号，现场没有人回应，可怜呐。终是曲子终曱散，狗薪水无处觅，蟑螂下尽一场梦[躺手]"
    text2 = "香港独分子颠倒是非黑白！毫无廉耻！毫无智商朝！愚蠢邪恶透顶！几年港独，台独，FLG，国内带路党有强烈的合流趋势！"
    text3 = "有一件事就不能说的例如光复香港时代革命五大诉求空缺一不可我就不buy的"
    print(text1 + "\n" + mySent.get_sentiment(text1).__str__())
    print(text2 + "\n" + mySent.get_sentiment(text2).__str__())
    print(text3 + "\n" + mySent.get_sentiment(text3).__str__())