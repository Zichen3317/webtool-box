# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/18
#           Version:
#             Description: 爬取Html框架（用类重写）
# ==========================================
# 导入库
import requests
from bs4 import BeautifulSoup
import streamlit as st
Version = '0.1'


class GetData:
    '''
    爬取目标HTML页面并返回页面原始Body
    '''

    def __init__(self, url=None, refer="https://cn.bing.com/", cookie=None):
        self.refer = refer
        self.url = url
        self.cookie = cookie

    def GetHTMLDATA(self):
        '''
        用于爬取目的网址HTML网页内容 的函数
        参数：
        url 需要爬取内容的网址

        并从网页中爬取数据，并保存在一个列表中
        需要寻找对应数据请看示例：

        用 Beautiful Soup 方法解析网页结构，用find（）找到对应的标签。
        data = body.find('div', {'class': 'info clearfix'})  # 找到对应的标签

        '''
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
                "Referer": self.refer,
                "cookie": self.cookie}
            r = requests.get(self.url, timeout=30,
                             headers=header)  # 用requests抓取网页信息
            r.raise_for_status()  # 可以让程序产生异常时停止程序
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'html.parser')  # 用BeautifulSoup库解析网页
            body = soup.body
            return body
        except:
            st.error('ERROR')
            pass
