# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/17
#           Version:
#             Description: 留言板
# ==========================================
import traceback
import streamlit as st
from deta import Deta
from datetime import datetime
st.set_page_config(
    page_title="梓宸の留言板",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# 试验版应用"
    })

version = '0.1'
PushDeer_key = st.secrets['PushDeer_key']
deta = Deta(st.secrets["deta_key"])
db = deta.Base('WEBToolBOX-streamlit-Message-Board')
# 获取数据库表头（字典形式）
Message_Data = db.fetch().items
Message_Dict = {}


st.markdown("## 📋梓宸の留言板📋\n版本号:%s" % version)

try:
    for i in Message_Data:
        Message_Dict[(i['hometown'])] = {'key': i['key'],
                                         'name': i['name']}
    with st.expander("留言"):
        for i in Message_Data:
            st.markdown("[%s] %s" % (i['name'], i['hometown']))
except:
    st.error("留言信息读取异常：\n%s" % traceback.format_exc())


class Message:
    '''
    上传、删除留言
    需要传入数据：
    content:str 留言
    name:str 留言人信息(最好是名称)
    PASSWORD_Delete:str 删除留言时所需的权限密码
    '''

    def __init__(self, name, content=None, PASSWORD_Delete=None):
        '''
        在删除留言时 content、PASSWORD_Delete 可以不传入
        '''
        # 信息传入先赋予Time属性
        self.Time = str(datetime.today()).split('.')[0]
        self.name = name
        self.content = content

# 上传留言
    def Create(self):
        db.put({"name": "[{Time}]|{Name}".format(Time=self.Time,
                                                 Name=self.name),
                "hometown": self.content})
        st.success("✔上传成功！")
        st.snow()

# 删除留言

    def Delete(self):
        if self.PASSWORD_Delete == st.secrets['author_password']:
            try:
                for i in self.content:
                    db.delete(Message_Dict[i]["key"])
                st.success("✔已删除")
            except:
                st.error(traceback.format_exc())
        else:
            st.warning("❌未获取删除权限！请检查权限密码是否正确！")


with st.container():
    col_L, col_R = st.columns(2)
    with col_L:
        st.markdown("##### 创建留言")
        with st.form("创建留言"):
            Message_Name = st.text_input("如何称呼您？")
            Message_Create = st.text_area("留言内容")
            Message_Create_submitted = st.form_submit_button('发送')
            if Message_Create_submitted:
                M = Message(content=Message_Create,
                            name=Message_Name)
                M.Create()
    with col_R:
        st.markdown("##### 删除留言")
        with st.form("删除留言"):
            PASSWORD_Delete = st.text_input("权限密码")
            Message_MutiSelect = st.multiselect(
                "留言列表", Message_Dict.keys())
            Message_Delete_submitted = st.form_submit_button('删除')
            if Message_Delete_submitted:
                M = Message(content=Message_MutiSelect,
                            PASSWORD_Delete=PASSWORD_Delete)
                M.Delete()
