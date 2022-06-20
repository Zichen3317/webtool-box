
# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/12
#           Version:
#             Description: 工具箱web页面主函数
# ==========================================
# 函数依赖库
from MOD import Douban_Film
from MOD import PushDeer
from MOD import bilibili_personal_information
from MOD import bilibili_public_liveStatus
from MOD import bilibili_private_liveStatus
from MOD import NeteaseCloudGames_autocheckin_index
from MOD import QQkg
import pandas as pd
import streamlit as st
import json
import os
import re
import ssl
import traceback
from datetime import datetime
from re import sub
from urllib import request
import pytz
import sys  # 导入sys模块
sys.setrecursionlimit(2500)  # 将默认的递归深度修改
# 界面依赖库
# MOD
version = '🖥0.0.4🖥'
# 输出格式设置
ssl._create_default_https_context = ssl._create_unverified_context
# 主页面设置
st.set_page_config(
    page_title="梓宸の工具箱",
    page_icon="🍦",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# 试验版应用"
    }
)
PushDeer_key = st.secrets['PushDeer_key']


# 网易云获取歌词主函数


def Netease_URL_Processing(Url, TYPE):
    '''
    将输入的歌曲链接进行处理得到想要的歌曲链接

    Url 链接,EG.https://music.163.com/#/song?id=1353531882
    TYPE 类型；分为
    [
        SONG:单曲
        LIST:歌单
    ]
    '''
    if TYPE == 'SONG':
        patternID = re.compile(r'[id=]\d+[&]')  # 查找数字
        # 单曲下载
        songID = re.sub(r'[=]|[&]', '', patternID.findall(Url)[0])
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
    elif TYPE == 'LIST':
        try:
            patternID = re.compile(r'[id=]\d+[&]')  # 查找数字
            playListID = re.sub(
                r'[=]|[&]', '', patternID.findall(Url)[0])
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

                SONGLIST_DATA_GET.progress(round(start_num_01/total_num, 1))

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
                SONGLIST_Download.progress(round(start_num_02/total_num, 1))

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
                            Netease_URL_Processing(songList, 'LIST')
                            # [[歌曲1作者,歌曲1名,歌曲1的ID,歌曲1所属平台],[歌曲2作者,歌曲2名,歌曲2的ID,歌曲2所属平台],...]
            st.success(
                '下载完成✓\n文件已保存到本程序%s所在目录下' % TIME)
        except:  # 错误报错
            st.error(traceback.format_exc())


# 主页面
# 主标题
st.markdown('# **梓宸の工具箱** \n**版本号：** *%s*' % version)

# 发送信息给zc
with st.expander("发信息给梓宸（可供本地/云服务器使用）"):
    with st.form('发送信息'):
        text = str(st.text_input('信息'))
        PushDeer_Sent_buttom = st.form_submit_button("发送")
        if PushDeer_Sent_buttom:
            try:
                PushDeer.PushDeer_Sent(PushDeer_key, text)
                st.success('信息已发送✌')
            except:
                st.error(traceback.format_exc())

# 网易云歌词下载
# 可伸缩拓展容器套表单
with st.expander("网易云歌词下载（仅供本地服务器使用）"):
    with st.form("网易云歌词下载"):
        URL_input = st.text_input('歌曲/歌单链接/id', '请在此处输入链接/id')

        TYPE_option = st.selectbox(
            '链接/id类型',
            ("单曲", "歌单"))
        # 表单信息提交按钮
        submitted = st.form_submit_button("开始下载！！！")
        if submitted:
            try:
                # 显示表单信息并进行信息转换
                st.info("URL:%s 【%s】\nTYPE:%s 【%s】" %
                        (URL_input, type(URL_input), TYPE_option, type(TYPE_option)))
                if TYPE_option == '单曲':
                    Netease_URL_Processing(URL_input, 'SONG')
                elif TYPE_option == '歌单':
                    Netease_URL_Processing(URL_input, 'LIST')

            except:
                e = RuntimeError(traceback.format_exc())
                st.exception(e)

# MOD01 - 网易云游戏签到函数


def NeteaseCloudGames_autocheckin(cookies):
    if cookies == "" or cookies == []:
        st.error('[网易云游戏自动签到]未设置cookie！')
    sign_url = 'https://n.cg.163.com/api/v2/sign-today'
    current = 'https://n.cg.163.com/api/v2/client-settings/@current'
    st.info('检测到{}个账号，即将开始签到！'.format(len(cookies)))
    success = []
    failure = []
    msg = []
    for i in cookies:
        cookie = i
        autherror = False
        signerror = False
        sign_return = None
        me = None
        try:
            me = NeteaseCloudGames_autocheckin_index.getme(current, cookie)
        except:
            message = '第{}个账号验证失败！请检查Cookie是否过期！'.format(
                cookies.index(i) + 1)
            failure.append(cookie)
            msg.append(message)
            autherror = True

        if me.status_code != 200 and not autherror:
            message = '第{}个账号验证失败！请检查Cookie是否过期！'.format(
                cookies.index(i) + 1)
            failure.append(cookie)
            msg.append(message)
        elif me.status_code == 200:
            try:
                sign_return = NeteaseCloudGames_autocheckin_index.signin(
                    sign_url, cookie)
            except:
                message = '第{}个账号签到失败，回显状态码为{}，具体错误信息如下：{}'.format(
                    cookies.index(i) + 1, sign_return.status_code, sign_return.text)
                failure.append(cookie)
                msg.append(message)
                signerror = True

            if sign_return.status_code == 200:
                message = '第{}个账号签到成功！'.format(cookies.index(i) + 1)
                success.append(cookie)
                msg.append(message)
            elif not signerror:
                message = '第{}个账号签到失败，回显状态码为{}，具体错误信息如下：{}'.format(
                    cookies.index(i) + 1, sign_return.status_code, sign_return.text)
                failure.append(cookie)
                msg.append(message)
    outputmsg = str(msg).replace("[", '').replace(
        ']', '').replace(',', '<br>').replace('\'', '')
    Mailinfomsg = '''
    =网易云游戏自动签到脚本=
    今日签到结果如下：
    ✅成功数量：{0}/{2}
    ❌失败数量：{1}/{2}
    具体情况如下：
    {3}

    '''.format(len(success), len(failure), len(cookies), outputmsg)
    st.success(Mailinfomsg)
    # 用PushDeer发送
    PushDeer.PushDeer_Sent(PushDeer_key, Mailinfomsg)
    if (len(failure) != 0):
        st.error("[网易云游戏自动签到]脚本运行错误，具体请参见日志！")


# MOD01 - 网易云游戏签到模块
with st.expander("网易云游戏签到（可供本地/云服务器使用）"):
    if st.button('帮梓宸签到'):
        try:
            NeteaseCloudGames_autocheckin(['Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsIm5iZiI6MTY1NDgxMzY2OCwianRpIjoiY2Q0ZDY3ZWMtOTI3MC00OGY3LTk3MTktMTg3ZmYyNzEyMjIwIiwiaWRlbnRpdHkiOiI2MmEyMDMwOTg0YTk5YjhhY2FkN2E3MDkiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNjU0ODEzNjY4LCJ1c2VyX2NsYWltcyI6eyJudW1iZXIiOjQ5MDYyNDM2MCwic2FsdCI6NjgsInRpbWVzdGFtcCI6MTY1NDgxMzY2OH19.laEepzz2TFvntOZQqjNkyy_fkE3LfLpEO4jsx3q7cCQ'])
        except:
            st.error(traceback.format_exc())

    with st.form('网易云游戏签到'):
        cookies = str(st.text_input('请输入cookie;多个cookie请用|隔开', ''))
        cookies_TYPE = st.radio(
            "cookie个数", ('1', '>1'))
        submitted_checkin = st.form_submit_button('→签到←')

        if submitted_checkin:
            try:
                # 提交的时候按多个/单个cookie来分别处理
                if cookies_TYPE == '1':
                    NeteaseCloudGames_autocheckin([cookies])
                elif cookies_TYPE == '>1':
                    cookies = cookies.split('|')
                    NeteaseCloudGames_autocheckin(cookies)
            except:
                st.error(traceback.format_exc())

# MOD02 - 查询B站UP开播情况
with st.expander("B站UP开播情况（可供本地/云服务器使用）"):
    bili_public_test_button = st.button('测试')
    with st.form('利用cookie获取个人关注的直播开播情况'):
        bili_private_cookie = str(st.text_input('请输入cookie', ''))
        bili_private_submit = st.form_submit_button('>获取<')

        if bili_private_submit:
            try:
                bilibili_personal_data = bilibili_personal_information.GetData(
                    bili_private_cookie)
                st.info('获取UP直播信息中...')
                bilibili_private_data = bilibili_private_liveStatus.GetData(
                    bili_private_cookie)
                st.success('已获取UP直播信息✓')
                # 用户信息
                st.markdown("### %s (%s)关注的UP开播信息" % (
                    bilibili_personal_data['name'], bilibili_personal_data['uid']))
                # 大粗体显示指标
                st.metric(label='已开播人数', value=len(
                    bilibili_private_data['uid']), delta_color="inverse", delta=None)
                # 直播UP信息显示
                st.table(bilibili_private_data)

            except:
                st.error(traceback.format_exc())

    if bili_public_test_button:
        try:
            st.info('获取UP直播信息中...')
            bili_public_data = bilibili_public_liveStatus.index()
            st.success('已获取UP直播信息✓')
            # 直播UP信息显示
            st.table(bili_public_data)
        except:
            st.error(traceback.format_exc())

# MOD02 - Extension - 由cookie查看个人基本信息
with st.expander('B站个人信息查看（可供本地/云服务器使用）'):
    with st.form('利用cookie获取个人信息'):
        bili_private_cookie = str(st.text_input('请输入cookie', ''))
        bili_private_submit = st.form_submit_button('>获取<')

        if bili_private_submit:
            try:
                bilibili_personal_data = bilibili_personal_information.GetData(
                    bili_private_cookie)
                st.markdown("## %s(%s) 的个人信息 " % (
                    bilibili_personal_data['name'], bilibili_personal_data['uid']))
                st.markdown("#### 等级:%s" % bilibili_personal_data['level'])
                st.markdown("#### 硬币:%s" % bilibili_personal_data['coin'])
            except:
                st.error(traceback.format_exc())

# 先获取城市信息
City_Dict = Douban_Film.Film().City_GET_DATA()
# MOD03 - 豆瓣正在/即将上线电影查询
with st.expander('豆瓣正在/即将上线电影查询'):
    with st.form('DouBanFilm_GET'):
        CitySelect = st.text_input('输入要查看的城市名称')
        submitted = st.form_submit_button('点击查看')
        if submitted:
            try:
                ComingFilmData = Douban_Film.Film(
                    city=City_Dict[CitySelect]).Upcoming_GET_FILM()
                ReleasingFilmData = Douban_Film.Film(
                    city=City_Dict[CitySelect]).NowPlaying_GET_FILM()
                st.markdown("## [%s] 正在上映" % CitySelect)
                st.dataframe(ReleasingFilmData)
                st.markdown("## [%s] 即将上映" % CitySelect)
                st.dataframe(ComingFilmData)
            except KeyError:
                st.warning(traceback.format_exc())

#MOD04 -全民K歌歌曲解析
with st.expander('全民K歌歌曲解析'):
    with st.form('QQkg'):
        SongURL = st.text_input('歌曲分析链接')
        submitted = st.form_submit_button('解析')
        if submitted:
            try:
                Song_Dict = QQkg.SONG(url=SongURL).GETData()
                st.success('✌解析完毕')
                try:
                    st.markdown("### {SongName} - {SingerName} (Cover:{CovererName})\n歌曲链接: [点击打开]({Url})".format(
                        SongName=Song_Dict['Song_Name'],
                        SingerName=Song_Dict['Singer_Name'],
                        CovererName=Song_Dict['Coverer_Name'],
                        Url=Song_Dict['Song_URL']))
                except:
                    st.markdown('#### 歌曲信息获取异常，仅获取到歌曲链接!\n歌曲链接: [点击打开]({Url})'.format(
                     Url=Song_Dict['Song_URL']   
                    ))
            except:
                st.error(traceback.format_exc())
