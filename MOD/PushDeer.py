# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/14
#           Version:
#             Description: PushDeer发送模块
# ==========================================
import requests as r
Version = '0.1'


def PushDeer_Sent(key, message):
    url = "https://api2.pushdeer.com/message/push?pushkey=%s&text=%s" % (
        key, message)
    r.get(url)
    return True
