# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/15
#           Version:
#             Description: 用来发布文章的
# ==========================================
import streamlit as st
from deta import Deta
st.set_page_config(
    page_title="梓宸のBlog",
    page_icon="📖",
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
# 获取数据库表头（字典形式）
Article_Data = db.fetch().items
st.metric('已发布文章数', len(Article_Data))
try:
    for i in Article_Data:
        with st.expander(i['name']):
            st.markdown(i['hometown'])
except ValueError:
    pass
except KeyError:
    pass
