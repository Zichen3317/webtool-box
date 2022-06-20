# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/15
#           Version:
#             Description: 引导页面
# ==========================================
import streamlit as st
from datetime import datetime
# 启动服务
print('[%s]服务已启动✓' % datetime.today())

st.set_page_config(
    page_title="🏡梓宸の空间🏡",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# 试验版应用"
    }
)
Information_Tuple = {'导航': ['Home',
                            'ToolBox',
                            'Article',
                            'Message Board',
                            'Article WriteTool'],
                     '说明': ['主页',
                            '工具箱',
                            '发布的文章',
                            '留言板',
                            '写作工具']}

st.markdown(
    "# 🎉欢迎来到梓宸の实验室🎉\n ### 👈请从侧边栏进入\n[项目源码（Github）](https://github.com/Zichen3317/webtool-box/edit)")
with st.container():
    st.markdown('***')
    st.markdown('📜侧边栏导航说明📜')
    st.table(Information_Tuple)
