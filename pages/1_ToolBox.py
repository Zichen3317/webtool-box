
# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/12
#           Version:
#             Description: 工具箱web页面主函数
# ==========================================
# 函数依赖库
from MOD import PushDeer
from MOD import bilibili_personal_information
from MOD import bilibili_public_liveStatus
from MOD import bilibili_private_liveStatus
from MOD import NeteaseCloudGames_autocheckin_index
from MOD import QQkg
from MOD import NeteaseMusic
from MOD import ArkNights_SearchInformation_Webtoolbox
from MOD import CSVTool
from time import strftime, localtime
from datetime import datetime
import streamlit as st
import ssl
import traceback
import sys  # 导入sys模块
import random
sys.setrecursionlimit(2500)  # 将默认的递归深度修改
# 界面依赖库
# MOD
version = '🖥0.0.8({LastModify_Time})🖥'.format(
    LastModify_Time=str(datetime.today()).split('.')[0])
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


# 主页面
# 主标题
st.markdown('# **梓宸の工具箱** \n**版本号：** *%s*' % version)

with st.expander("抽奖工具（可供本地/云服务器使用）"):
    with st.form('抽奖'):
        TotalNum = str(st.text_input('总人数'))
        SelectNum = str(st.text_input('抽取人数'))
        PushDeer_Random_Start = st.form_submit_button("抽取")
        if PushDeer_Random_Start:
            try:
                st.success('抽取结果:%s' % random.sample(
                    range(1, int(TotalNum)+1), int(SelectNum)))
            except:
                st.error(traceback.format_exc())

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
                    NeteaseMusic.Music(
                        URL_input, 'SONG').Netease_URL_Processing()
                elif TYPE_option == '歌单':
                    NeteaseMusic.Music(
                        URL_input, 'LIST').Netease_URL_Processing()

            except:
                e = RuntimeError(traceback.format_exc())
                st.exception(e)

# MOD01 - 网易云游戏签到模块
with st.expander("网易云游戏签到（可供本地/云服务器使用）"):
    if st.button('帮梓宸签到'):
        try:
            Mailinfomsg = NeteaseCloudGames_autocheckin_index.Autocheckin(
                ['Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsIm5iZiI6MTY1NDgxMzY2OCwianRpIjoiY2Q0ZDY3ZWMtOTI3MC00OGY3LTk3MTktMTg3ZmYyNzEyMjIwIiwiaWRlbnRpdHkiOiI2MmEyMDMwOTg0YTk5YjhhY2FkN2E3MDkiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNjU0ODEzNjY4LCJ1c2VyX2NsYWltcyI6eyJudW1iZXIiOjQ5MDYyNDM2MCwic2FsdCI6NjgsInRpbWVzdGFtcCI6MTY1NDgxMzY2OH19.laEepzz2TFvntOZQqjNkyy_fkE3LfLpEO4jsx3q7cCQ'])
            st.success("签到成功✌")
            PushDeer.PushDeer_Sent(PushDeer_key, Mailinfomsg)
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
                    Mailinfomsg = NeteaseCloudGames_autocheckin_index.Autocheckin([
                                                                                  cookies])
                    st.success('[单]签到成功✌')
                    PushDeer.PushDeer_Sent(PushDeer_key, Mailinfomsg)

                elif cookies_TYPE == '>1':
                    cookies = cookies.split('|')
                    Mailinfomsg = NeteaseCloudGames_autocheckin_index.Autocheckin(
                        cookies)
                    st.success('[多]签到成功✌')
                    PushDeer.PushDeer_Sent(PushDeer_key, Mailinfomsg)

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
                bilibili_personal_data = bilibili_personal_information.Information(bili_private_cookie).GetData()#这个库是个类，其他B站调用库只是函数
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
                bilibili_personal_data = bilibili_personal_information.Information(
                    cookie=bili_private_cookie).GetData()
                st.markdown("## {Name} (UID:{UID}) 的个人信息\n - [等级] {Level}({current_exp}/{next_exp})".format(Name=bilibili_personal_data["profile"]['name'],
                                                                                                            UID=bilibili_personal_data[
                    "profile"]['mid'],
                    Level=bilibili_personal_data[
                    'level_info']['current_level'],
                    current_exp=bilibili_personal_data[
                    'level_info']['current_exp'],
                    next_exp=bilibili_personal_data['level_info']['next_exp']))
                st.markdown(" - [绑定情况] \n|项目|状态|\n|:--:|:--:|\n|邮箱|{email_status}|\n|电话|{tel_status}|\n|实名认证|{identification}|".format(
                    email_status=bilibili_personal_data["profile"]['email_status'],
                    tel_status=bilibili_personal_data["profile"]['tel_status'],
                    identification=bilibili_personal_data["profile"]['identification']
                ))
                st.markdown("#### [入站时间] %s" % strftime("%Y-%m-%d-%a %I:%M:%S(%p)",
                                                        localtime(bilibili_personal_data["profile"]['jointime'])))

            except:
                st.error(traceback.format_exc())

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
