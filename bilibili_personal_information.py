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


def GetData(cookie):
    url = "https://api.bilibili.com/x/web-interface/nav"  # 请求的url
    headers = {  # 请求的头部
        "referer": "https://t.bilibili.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
        "cookie": "%s" % cookie,
    }

    req = request.Request(url=url, headers=headers)  # GET无data项
    res = request.urlopen(req)
    res = str(res.read(), encoding='utf-8')  # 将返回的bytes类型转为str类型
    data = json.loads(res).get('data')  # 如果是json/dict类型,这一步可以转为dict类型,前提是从str转
    return {'name': data['uname'],
            'uid': data['mid'],
            'coin': data['money'],
            'level': data['level_info']['current_level']}
