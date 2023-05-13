# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/16
#           Version:
#             Description: 写文章用的辅助工具
# ==========================================
import traceback
from datetime import datetime
import streamlit as st
from deta import Deta
from MOD import PushDeer
import pytz
# 主页面设置
st.set_page_config(
    page_title="梓宸の写作工具",
    page_icon="🖋",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# 试验版应用"
    })

# 链接数据库
deta = Deta(st.secrets["deta_key"])
db = deta.Base('demo001-WEBToolBOX-streamlit-Article')
PushDeer_key = st.secrets['PushDeer_key']
# 获取数据库数据 [{}]
Article_Dict = {}

try:
    Article_Data = db.fetch().items
    for i in Article_Data:
        Article_Dict[i['name']] = {'key': i['key'],
                                   'content': i['hometown']}
except KeyError:
    pass
except ValueError:
    pass
Tool_Version = '0.3.1'
st.markdown("## 🖋写作工具🖋\n *版本号:%s*" % Tool_Version)
tab1, tab2, tab3 = st.tabs(["🖊写作", "🖌修改", "✂删除"])
with tab1:
    st.markdown("### 🖊写作")
    with st.form('文章必要信息录入'):
        Author_PASSWORD_New = st.text_input('权限密码')
        Article_Name = st.text_input('文章名称')
        Article_Author = st.text_input('作者')
        Article_Content = st.text_area('文章内容')
        preview = st.form_submit_button('预览👁')
        submitted = st.form_submit_button('发布文章')
        if submitted:
            if Author_PASSWORD_New == st.secrets["author_password"]:
                submitted_Time = str(datetime.now(pytz.timezone('Asia/Shanghai'))).split('.')[
                    0].split(' ')[0]
                try:
                    st.info('开始写入 %s-%s' % (Article_Author, Article_Name))
                    result = db.put({
                        "name": "%s|%s-%s" % (submitted_Time, Article_Author, Article_Name),
                        "hometown": str(Article_Content)
                    })
                    st.success('✔写入成功！')
                    st.balloons()
                    # 推送信息
                    PushDeer.PushDeer_Sent(PushDeer_key, "[{Time}] - {Name} - 已上传".format(
                        Time=str(datetime.now(pytz.timezone(
                            'Asia/Shanghai'))).split('.')[0],
                        Name="%s|%s-%s" % (submitted_Time,
                                           Article_Author, Article_Name)
                    ))
                except:
                    st.error('请检查数据库是否在线')
                    st.error(traceback.format_exc())
            else:
                st.warning("❌未获取上传权限！请检查权限密码是否正确！")

with tab2:
    st.markdown("### 🖌修改")
    with st.form('需修改文章提交'):
        Author_PASSWORD_Modify = st.text_input('权限密码')
        Article_Select = st.selectbox(
            "数据库文章列表", Article_Dict.keys())
        Article_Modify_view = st.form_submit_button('查看')
        Article_Modify_Content = st.text_area(
            label='修改后的文章内容', value='')

        Article_Modify_preview = st.form_submit_button('预览')
        Article_Modify_submitted = st.form_submit_button('修改')

        if Article_Modify_submitted:
            if Author_PASSWORD_Modify == st.secrets["author_password"]:
                Modify_Time = str(datetime.now(pytz.timezone('Asia/Shanghai'))).split('.')[
                    0].split(' ')[0]
                try:
                    # TIP：文章名称格式为 创建日期|作者-文章名，上传修改版本后需要把创建日期替换掉
                    st.info('开始修改%s' %
                            Article_Select.split('|')[-1])
                    # 修改时需附带上传原文章key
                    # 注意在重命名时，由于原文章名中包含了时间，故需要将原时间切除后加入新时间
                    result = db.put({
                        "name": "%s|%s" % (Modify_Time, Article_Select.split('|')[-1]),
                        "hometown": '- *[修改时间] %s* \n%s' % (Modify_Time, Article_Modify_Content)}, Article_Dict[Article_Select]['key'])
                    st.success('✔修改成功！')
                    st.balloons()
                    # 推送信息
                    PushDeer.PushDeer_Sent(PushDeer_key, "[{Time}] - {Name} - 进行了修改".format(
                        Time=str(datetime.now(pytz.timezone(
                            'Asia/Shanghai'))).split('.')[0],
                        Name="%s|%s" % (
                            Modify_Time, Article_Select.split('|')[-1])
                    ))
                except:
                    st.error(traceback.format_exc())
            else:
                st.warning("❌未获取修改权限！请检查权限密码是否正确！")

# 删除文章操作窗口
with tab3:
    st.markdown("### ✂删除")
    with st.form('删除指定文章'):
        Author_PASSWORD_Delete = st.text_input('权限密码')
        # 多选框，返回列表
        Article_MutiSelect = st.multiselect(
            "数据库文章列表", Article_Dict.keys())

        Article_Delete_preview = st.form_submit_button('预览')
        Article_Delete_submitted = st.form_submit_button('删除')

        if Article_Delete_submitted:
            if Author_PASSWORD_Delete == st.secrets["author_password"]:
                try:
                    Delete_Message = ''
                    for i in Article_MutiSelect:
                        result = db.delete(Article_Dict[i]['key'])
                        Delete_Message = Delete_Message+'已删除:%s\n' % i
                    st.info(Delete_Message)
                    PushDeer.PushDeer_Sent(PushDeer_key, "[{Time}] - {Message} - 已删除".format(
                        Time=str(datetime.now(pytz.timezone(
                            'Asia/Shanghai'))).split('.')[0],
                        Message=Delete_Message)
                    )

                except:
                    st.error(traceback.format_exc())
            else:
                st.warning("❌未获取删除权限！请检查权限密码是否正确！")


# 中部是预览窗口，需要放在最后
with st.container():
    st.markdown("***")
    st.markdown("### 👁预览界面")

# 写作时的文章预览
    if preview:
        preview_Time = str(datetime.now(pytz.timezone('Asia/Shanghai'))).split('.')[
            0].split(' ')[0]

        st.markdown('\n ## %s|%s-%s' %
                    (Article_Name, Article_Author, preview_Time))
        st.markdown(Article_Content)
# 修改时的文章预览

    if Article_Modify_view:
        st.markdown("## 修改前文章:")
        st.text("%s " %
                Article_Dict[Article_Select]['content'])
        st.markdown("***")
        st.markdown(' ## %s' % Article_Select)
        st.markdown(Article_Dict[Article_Select]['content'])
    if Article_Modify_preview:
        st.markdown(Article_Modify_Content)

# 删除时的文章预览
    if Article_Delete_preview:
        for i in Article_MutiSelect:
            with st.expander(i):
                st.markdown(Article_Dict[i]['content'])
