# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/07/08
#           Version:
#             Description: 爬取B站热门话题
# ==========================================
import traceback
from urllib import request
import json


class Topic():
    def __init__(self, Size=6, COOKIE='None'):
        # 爬取的链接
        self.Url = 'https://app.bilibili.com/x/topic/web/dynamic/rcmd?source=Web&page_size=%s' % Size
        self.headers = {
            "cookie": COOKIE,
        }

    def Get(self):
        OriginalData = json.loads(
            str(request.urlopen(request.Request(url=self.Url, headers=self.headers)).read(), encoding='utf-8'))
        if OriginalData["code"] == '-400':
            return "ERROR"
        elif OriginalData["code"] == '0':
            DATA = OriginalData['data']['topic_items']
            return DATA
