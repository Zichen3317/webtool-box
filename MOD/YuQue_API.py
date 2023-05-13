# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/07/31
#           Version:
#             Description: 对接语雀API，将功能简化
# ==========================================
import json
import traceback
from urllib import request
import streamlit as st
from datetime import datetime

class YuQue():
    def __init__(self, Token, Namespace, DOCName):
        '''
        Token 语雀个人Token
        REPO 知识库路径 repo/docs
        DOCName 文档名称
        '''
        self.Token = Token
        self.Namespace = Namespace
        self.DOCName = DOCName

    def GetDocDetail(self):
        DocDetail_url = 'https://www.yuque.com/api/v2/repos/%s/docs/%s?raw=1' % (
            self.Namespace, self.DOCName)
        # 加标头
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36",
            "X-Auth-Token": self.Token,
        }
        # 获取响应的json字符串
        # 把json转换成字典
        myjson = json.loads(request.urlopen(request.Request(
            url=DocDetail_url, headers=header)).read().decode('utf-8'))

        try:
            data = {}
            data["title"] = myjson['data']["title"]
            data['updated_time'] = myjson['data']["updated_at"]
            data['user_name'] = myjson['data']["book"]["user"]["name"]
            data['content_md'] = myjson['data']["body"]
            print('[%s]已连接语雀API✓' % datetime.today())
        except:
            st.error(traceback.format_exc())
            try:
                if myjson["status"] == 400:
                    st.info('请求的参数不正确，或缺少必要信息')
                elif myjson["status"] == 401:
                    st.info('需要用户认证的接口用户信息不正确')
                elif myjson["status"] == 403:
                    st.info('缺少对应功能的权限')
                elif myjson["status"] == 404:
                    st.info('数据不存在，或未开放')
                elif myjson["status"] == 500:
                    st.info('服务器异常')
            except:
                pass

        return data
