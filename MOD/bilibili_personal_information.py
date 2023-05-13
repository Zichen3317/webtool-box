# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/14
#           Version:
#             Description: 通过cookie获取个人信息
# ==========================================
from urllib import request
import json

Version = '0.2'


class Information:
    def __init__(self, cookie):
        self.cookie = cookie

    def GetData(self):
        '''
        由cookie获取个人基本信息（不包括入站时间）
        '''
        url = "https://member.bilibili.com/x2/creative/h5/calendar/event?ts=0"  # 请求的url
        headers = {  # 请求的头部
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
            "cookie": "%s" % self.cookie,
        }

        req = request.Request(url=url, headers=headers)  # GET无data项
        res = request.urlopen(req)
        res = str(res.read(), encoding='utf-8')  # 将返回的bytes类型转为str类型
        # 如果是json/dict类型,这一步可以转为dict类型,前提是从str转
        data = json.loads(res).get('data')["pfs"]
        return data
