# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/22
#           Version:
#             Description: 更新日志
# ==========================================
import streamlit as st

st.set_page_config(
    page_title="梓宸の更新日志",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# 试验版应用"
    })

st.markdown("""
# WebToolBox **更新日志**

## 1.0

* [demo001-WEBToolBOX_streamlit](https://github.com/Zichen3317/webtool-box) 正式开始建设
* 初始拥有**ToolBox**页面，将原有demo中的***网易云歌词下载***功能迁移至此

## 1.1

### ToolBox

* 接入**Pushdeer**模块，开发***发送信息***功能
* 将原有demo中的***网易云游戏签到***功能迁移至此
* 将原有demo中的***查询B站信息***功能迁移至此

## 1.2

* 新增 **Article[文章显示页面]** 与 **Article WriteTool[文章修改工具]**

### Article WriteTool

* 接入**Deta** 模块，开发**文章 写作、修改、删除** 功能
* 开发 ***密码限制*** 功能

## 1.3

* 使用 **Streamlit** 模块 中更新的 **Tab** 功能，对一些页面进行适应性改动

## 1.4

### Resource

* 接入**语雀API**
* 使用**语雀API** 实时更新资源站

## 1.4.1

### Resource

* 界面优化：将展示页面设为主页，**增加**  ***后台***  页面
* 新增 **缓存** 功能：主页显示的内容**从Deta数据库读取**而不采取 *直接向语雀API发送请求* 的方式（语雀API有**请求限量**，**5000次/h**）,站长可以在后台**使用权限密码刷新缓存**

## 1.4.1.1

### Article

* 界面优化：将文章按时间顺序排序，便于查看

## 1.4.1.2

### Tool_box

- 新增简单抽取工具


                """)
