# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/20
#           Version:
#             Description: 解析全民K歌歌曲
# ==========================================
from MOD import HTML_crawler
import re
import traceback
import streamlit as st

Version = '0.1'


class SONG:
    '''
    爬取全民k歌歌曲直链以及相关信息并返回
    '''

    def __init__(self, url):
        self.url = url
        self.DATA = HTML_crawler.GetData(
            self.url, refer='https://szfilehelper.weixin.qq.com/').GetHTMLDATA()

    def GETData(self):
        try:
            Data_Dict = {}
            DataBase = str(self.DATA.find(
                'script', {'type': "text/javascript"}).contents)

            Data_Dict['Song_URL'] = re.findall(
                r'"playurl":"(\S+)","playurl_video":', DataBase)[0]
            try:
                Data_Dict['Song_Name'] = re.findall(
                    r'"song_name":"(\S+)"', DataBase)[0].split(',')[0].replace('"', '')
            except:
                Data_Dict['Song_Name'] = re.findall(
                    r'"song_name":"(\S+)"', DataBase)[0]

            # 2022/06/20-23:36:53 用try分两种情况的目的：某些歌手的名字带()会导致正则匹配异常，
            # 但可以用另外一个正则表达式匹配到（但这位歌手名字中括号内部分获取不到）
            try:
                Data_Dict['Singer_Name'] = re.findall(
                    r'"singer_name":"(\S+)', DataBase)[0].split(',')[0].replace('"', '')
            except:
                Data_Dict['Singer_Name'] = re.findall(
                    r'"singer_name":"(\S+)', DataBase)[0]
            # 翻唱者名
            Data_Dict['Coverer_Name'] = re.findall(
                r'"nick":"(\S+)","', DataBase)[0].split(',')[0].replace('"', '')

            return Data_Dict
        except:
            st.error(traceback.format_exc())
