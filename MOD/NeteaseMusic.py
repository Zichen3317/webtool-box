# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/21
#           Version:
#             Description: 调用网易云音乐API实现歌词下载等功能
# ==========================================
import json
import os
import re
from urllib import request
import pytz
from datetime import datetime
import streamlit as st
import traceback


class Music:
    def __init__(self, url, TYPE):
        self.Url = url
        self.TYPE = TYPE

    def Netease_URL_Processing(self):
        '''
        将输入的歌曲链接进行处理得到想要的歌曲链接

        Url 链接,EG.https://music.163.com/#/song?id=1353531882
        TYPE 类型；分为
        [
            SONG:单曲
            LIST:歌单
        ]
        '''
        if self.TYPE == 'SONG':
            patternID = re.compile(r'[id=]\d+[&]')  # 查找数字
            # 单曲下载
            songID = re.sub(r'[=]|[&]', '', patternID.findall(self.Url)[0])
            # 网易云音乐歌词apif
            neteaseApiUrl_lyric = 'https://zichen-cloud-music-api.vercel.app/lyric?id=%s&realIP=116.25.146.177' % songID
            # 网易云音乐歌曲信息api
            neteaseApiUrl_detail = 'https://zichen-cloud-music-api.vercel.app/song/detail?ids=%s' % songID
            req_detail = request.Request(url=neteaseApiUrl_detail)
            # 获得歌手名-歌曲名，用于歌词写入
            res_detail = request.urlopen(req_detail)
            # 获取响应的json字符串
            str_json_detail = res_detail.read().decode('utf-8')
            # 把json转换成字典
            myjson_detail = json.loads(str_json_detail)
            # 从字典中获得歌曲的名字及作者/翻唱者
            songName = myjson_detail['songs'][0]['name']
            # 由于作者/翻唱者可能有多个故使用列表存储，最后用join拼接即可
            songAuthorLst = []
            for i in myjson_detail['songs'][0]['ar']:
                songAuthorLst.append(i['name'])

            # 由于作者/翻唱者之间用 / 隔开会导致文件命名时出错故将 / 替换成 , 但这样做也会使下载的歌曲文件
            # 无法正确被播放器识别，暂时的解决方法是给出提示让用户自己去改名
            if bool(re.search(r'[/]', i['name'])) == True:
                st.error('下载歌曲名带/号，请自行下载！！！')
            else:
                songAuthor = re.sub(
                    r'[/]', ',', ','.join(songAuthorLst))
                songDetail = '%s - %s' % (songAuthor, songName)

                # 获得歌词文本

                req_lyric = request.Request(url=neteaseApiUrl_lyric)
                res_lyric = request.urlopen(req_lyric)
                # 获取响应的json字符串
                str_json_lyric = res_lyric.read().decode('utf-8')
                # 把json转换成字典
                myjson_lyric = json.loads(str_json_lyric)
                # 从字典中获得歌词文本
                lyrics = myjson_lyric['lrc']['lyric']

                with open('./%s.lrc' % songDetail, 'w', encoding='utf-8') as f:
                    f.write(lyrics)
                st.success(
                    '下载完成✓\n文件已保存到本程序所在目录下')

        # 歌单
        elif self.TYPE == 'LIST':
            try:
                patternID = re.compile(r'[id=]\d+[&]')  # 查找数字
                playListID = re.sub(
                    r'[=]|[&]', '', patternID.findall(self.Url)[0])
                limit = 1001  # 歌单中歌曲信息获取数量限制
                # 网易云音乐歌单详细信息api
                neteaseApiUrl_playList = 'https://zichen-cloud-music-api.vercel.app/playlist/detail?id=%s' % playListID
                # 加标头
                header = {
                    "User-Agent": "mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
                }

                req_playList = request.Request(
                    url=neteaseApiUrl_playList, headers=header)
                res_playList = request.urlopen(req_playList)

                # 获取响应的json字符串
                str_json_playList = res_playList.read().decode('utf-8')
                # 把json转换成字典
                myjson_playList = json.loads(str_json_playList)

                # 逐个获取歌单内的歌曲名及相应作者/翻唱者
                songList = []
                # 用于计数显示当前过程的数字
                # 01 获取歌单歌曲详情时使用
                # 02 下载歌曲时使用
                start_num_01 = 1
                start_num_02 = 1
                total_num = len(
                    myjson_playList["playlist"]["trackIds"])  # 总歌单歌曲数

                st.info('歌单歌曲数:%s\n 开始获取歌单歌曲详情...' % str(total_num))
                SONGLIST_DATA_GET = st.progress(0)

                # 根据大佬所述，未登录状态下无法获取歌单完整曲目，但trackIds是完整的，故获取trackIds后逐个请求，但此方法效率较低
                for songTotal in myjson_playList["playlist"]["trackIds"]:
                    songID = songTotal['id']  # 获得歌曲id

                    # 网易云音乐歌词api
                    neteaseApiUrl_lyric = 'https://zichen-cloud-music-api.vercel.app/lyric?id=%s&realIP=116.25.146.177' % songID
                    # 网易云音乐歌曲信息api
                    neteaseApiUrl_detail = 'https://zichen-cloud-music-api.vercel.app/song/detail?ids=%s' % songID

                    req_detail = request.Request(url=neteaseApiUrl_detail)
                    res_detail = request.urlopen(req_detail)
                    # 获取响应的json字符串
                    str_json_detail = res_detail.read().decode('utf-8')
                    # 把json转换成字典
                    myjson_detail = json.loads(str_json_detail)
                    # 从字典中获得歌曲的名字及作者/翻唱者
                    # Tip：由于获取的歌曲名有\xa0不间断符号故使用join+split消除该符号
                    songName = "" .join(
                        myjson_detail['songs'][0]['name'].split())
                    # 由于作者/翻唱者可能有多个故使用列表存储，最后用join拼接即可
                    songAuthorLst = []
                    for i in myjson_detail['songs'][0]['ar']:
                        songAuthorLst.append(i['name'])
                    # 由于作者/翻唱者之间用 / 隔开会导致文件命名时出错故将 / 替换成 , 但这样做也会使下载的歌曲文件
                    # 无法正确被播放器识别，暂时的解决方法是给出提示让用户自己去改名
                        if bool(re.search(r'[/]', i['name'])) == True:
                            st.error('下载歌曲名带/号，请自行下载！！！')

                    songAuthor = re.sub(
                        r'[/]', ',', ','.join(songAuthorLst))
                    # 将 作者/翻唱者+歌曲名+歌曲ID 用元组形式存储并最终存储至列表中
                    # [[歌曲1作者,歌曲1名,歌曲1的ID,歌曲1所属平台],[歌曲2作者,歌曲2名,歌曲2的ID,歌曲2所属平台],...]
                    songList.append(
                        [songAuthor, songName, str(songID), 'netease'])

                    SONGLIST_DATA_GET.progress(
                        round(start_num_01/total_num, 1))

                    start_num_01 += 1

                st.json(str(songList))

                # 进度条
                st.info('开始下载歌词...')
                SONGLIST_Download = st.progress(0)
                # 将上述获取到的歌曲信息进行解析并下载
                TIME = str(datetime.now(pytz.timezone('Asia/Shanghai'))).split('.')[
                    0].replace(':', '-').replace(' ', '-')
                os.mkdir('./%s' % TIME)

                for songLst in songList:
                    songDetail = '%s - %s' % (songLst[0], songLst[1])
                    songID = songLst[2]
                    # 进度条显示
                    SONGLIST_Download.progress(
                        round(start_num_02/total_num, 1))

                    start_num_02 += 1
                    # 开始下载
                    # 网易云音乐歌词api
                    if songLst[3] == 'netease':
                        neteaseApiUrl_lyric = 'https://zichen-cloud-music-api.vercel.app/lyric?id=%s&realIP=116.25.146.177' % songID
                        # 出错后会重新循环，跳过已经保存的文件，提升效率，避免重复请求
                        if os.path.exists('./%s.lrc' % songDetail) == True:
                            pass
                        else:
                            try:
                                # 获得歌词文本
                                req_lyric = request.Request(
                                    url=neteaseApiUrl_lyric)
                                res_lyric = request.urlopen(req_lyric)
                                # 获取响应的json字符串
                                str_json_lyric = res_lyric.read().decode('utf-8')
                                # 把json转换成字典
                                myjson_lyric = json.loads(str_json_lyric)
                                # 从字典中获得歌词文本
                                lyrics = myjson_lyric['lrc']['lyric']

                                with open('./%s/%s.lrc' % (TIME, songDetail), 'w', encoding='utf-8') as f:
                                    f.write(lyrics)

                            except:
                                del songList[start_num_02-1]
                                # 注意这里的songUrl是列表
                                Music(url=songList, TYPE='LIST').Netease_URL_Processing()
                                # [[歌曲1作者,歌曲1名,歌曲1的ID,歌曲1所属平台],[歌曲2作者,歌曲2名,歌曲2的ID,歌曲2所属平台],...]
                st.success(
                    '下载完成✓\n文件已保存到本程序%s所在目录下' % TIME)
            except:  # 错误报错
                st.error(traceback.format_exc())
