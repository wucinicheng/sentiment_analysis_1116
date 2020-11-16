# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 21:38
# @Author  : CHAO
# @File    : main.py
# @Software: PyCharm

# from MySentimentAnalysis import MySentimentAnalysis
import re
import time

import pymysql

# mysql数据库参数
from sentiment_analysis_utils.Baidu import baiduSentimentAnalysis
from translate_API import baidu

# 连接数据库参数配置
HOST = "127.0.0.1"
USER = "root"
PASSWD = "qwertyuiop!@#$%^"
DB = "twitter"
CHARSET = "utf8"

# 百度情感分析模块参数
DEFAULT_AK = 'Uh3eqy7yCry5oNMYNqmoKvNg'  # 百度情感分析AI中的
DEFAULT_SK = 'RCmNQPQrB3m1ayDUhquUfPgjuwCsLNFd'  # 百度情感分析AI中的


# 创建连接
conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)
# 创建游标
cur = conn.cursor()

# 初始化粤语翻译模块和情感分析模块
trans = baidu.translate_baidu()  # 用百度速度很快
baiduSA = baiduSentimentAnalysis(DEFAULT_AK, DEFAULT_SK)


def createTable():
    '''
    创建数据库表
    :return:
    '''

    try:
        sql = '''
            DROP TABLE IF EXISTS `filtered_message`;

            CREATE TABLE `filtered_message` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `channel_id` int(40) NOT NULL,
              `message_id` varchar(100) NOT NULL,
              `url` varchar(250) DEFAULT NULL,
              `title` text,
              `user_id` varchar(100) DEFAULT NULL,
              `is_reteet` tinyint(4) DEFAULT NULL,
              `origin_user_name` varchar(100) DEFAULT NULL,
              `origin_message_id` varchar(100) DEFAULT NULL,
              `receiver_id` int(40) DEFAULT NULL,
              `create_time` varchar(100) DEFAULT NULL,
              `crawl_time` timestamp NULL DEFAULT NULL,
              `inpuTaskID` int(11) DEFAULT NULL,
              `favorited_count` int(11) DEFAULT NULL,
              `retweet_count` int(11) DEFAULT NULL,
              `all_text` text,
              `screen_name` varchar(100) DEFAULT NULL,
              `reply_to_status_id` varchar(100) DEFAULT NULL,
              `reply_to_screen_name` varchar(100) DEFAULT NULL,
              `other1` varchar(10) DEFAULT NULL,
              `other2` varchar(10) DEFAULT NULL,
              `mention_users` varchar(100) DEFAULT NULL,
              `keyword` varchar(255) DEFAULT NULL,
              `location` varchar(255) DEFAULT NULL,
              `picture_url` varchar(255) DEFAULT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `idx_message` (`message_id`) USING BTREE,
              KEY `idx_screen_name` (`screen_name`) USING BTREE,
              KEY `idx_screenName_createTime` (`create_time`,`screen_name`) USING BTREE
            ) ENGINE=InnoDB AUTO_INCREMENT=151360408 DEFAULT CHARSET=utf8;
        '''
        cur.execute(sql)
        conn.commit()
        print('create table ok!')
    except Exception as e:
        print(e)

def mySelectAll():
    try:
        select_sql = 'SELECT * FROM message'
        cur.execute(select_sql)
        infos = cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(e)
    return infos

def myInsertList(infos):

    new_list = []  # 新建一个空列表用来存储元组数据

    for info in infos:
        if len(new_list) > 300:
            break
        try:
            # lang = re.search(r'lang="(.*?)" .*', message[15], re.M|re.I) # 获取该条信息的语言,由于翻译效果不是很好，暂时不用
            time.sleep(1)  # 百度API的QPS限制
            text = trans.translate(info[4])
            polarity = baiduSA.get_sentiment(text)
            # print("{} {}".format(message[4], polarity))
            if text and polarity == '0':
                id = info[0]
                channel_id = info[1]
                message_id = info[2]
                url = info[3]
                title = info[4]
                user_id = info[5]
                is_reteet = info[6]
                origin_user_name = info[7]
                origin_message_id = info[8]
                receiver_id = info[9]
                create_time = info[10]
                crawl_time = info[11]
                inpuTaskID = info[12]
                favorited_count = info[13]
                retweet_count = info[14]
                all_text = info[15]
                screen_name = info[16]
                reply_to_status_id = info[17]
                reply_to_screen_name = info[18]
                other1 = info[19]
                other2 = info[20]
                mention_users = info[21]
                keyword = info[22]
                location = info[23]
                picture_url = info[24]

                tup = (id, channel_id, message_id, url, title, user_id, is_reteet, origin_user_name, origin_message_id
                                , receiver_id,create_time, crawl_time, inpuTaskID, favorited_count, retweet_count, all_text
                                , screen_name, reply_to_status_id, reply_to_screen_name, other1, other2, mention_users, keyword
                                , location, picture_url)
                new_list.append(tup)
        except Exception as e:
            print(e)
    print("*" * 5 + "generate my insert list ok" + "*" * 5)
    return new_list

def myInsert(newList):
    try:
        sql = "INSERT INTO filtered_message VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 要插入的数据
        cur.executemany(sql, newList)  # 执行插入数据

        conn.commit()
        cur.close()
        conn.close()
        print('insert ok')
    except Exception as e:
        print(e)

if __name__ == "__main__":

    createTable()
    infos = mySelectAll()
    newList = myInsertList(infos)
    myInsert(newList)


    # 查询、处理、并插入数据库新表

    # try:
    #     select_sql = 'SELECT * FROM message'
    #     cur.execute(select_sql)
    #     for message in cur.fetchall():
    #         # lang = re.search(r'lang="(.*?)" .*', message[15], re.M|re.I) # 获取该条信息的语言,由于翻译效果不是很好，暂时不用
    #         time.sleep(1)# 百度API的QPS限制
    #         text = trans.translate(message[4])
    #         polarity = baiduSA.get_sentiment(text)
    #         # print("{} {}".format(message[4], polarity))
    #         if text and polarity == '0':
    #             id = message[0]
    #             channel_id = message[1]
    #             message_id = message[2]
    #             url = message[3]
    #             title = message[4]
    #             user_id = message[5]
    #             is_reteet = message[6]
    #             origin_user_name = message[7]
    #             origin_message_id = message[8]
    #             receiver_id = message[9]
    #             create_time = message[10]
    #             crawl_time = message[11]
    #             inpuTaskID = message[12]
    #             favorited_count = message[13]
    #             retweet_count = message[14]
    #             all_text = message[15]
    #             screen_name = message[16]
    #             reply_to_status_id = message[17]
    #             reply_to_screen_name = message[18]
    #             other1 = message[19]
    #             other2 = message[20]
    #             mention_users = message[21]
    #             keyword = message[22]
    #             location = message[23]
    #             picture_url = message[24]
    #             insert_sql = "INSERT INTO filtered_message VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #             cur.execute(insert_sql, (id, channel_id, message_id, url, title, user_id, is_reteet, origin_user_name, origin_message_id
    #                         , receiver_id,create_time, crawl_time, inpuTaskID, favorited_count, retweet_count, all_text
    #                         , screen_name, reply_to_status_id, reply_to_screen_name, other1, other2, mention_users, keyword
    #                         , location, picture_url))
    #             conn.commit()
    #             print(text)
    #         continue
    #     print('共查询到：', cur.rowcount, '条数据。')
    #
    # except Exception as e:
    #     conn.rollback()
    #     print(e)
    #
    #
    # cur.close()
    # conn.close()