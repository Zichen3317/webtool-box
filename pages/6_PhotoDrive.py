# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/19
#           Version:
#             Description: 将照片上传至Deta
# ==========================================
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
import traceback
import streamlit as st
from deta import Deta
from urllib3.util import ssl_
ssl_.DEFAULT_CIPHERS = 'ALL'
# 主页面设置
st.set_page_config(
    page_title="梓宸のDeta网盘",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# 试验版应用"
    }
)
deta = Deta(st.secrets["deta_key"])
app = FastAPI()


class Photo:
    def __init__(self, DriveName, UpL_FilePath=None, DownL_FilePath=None):
        '''
        DriveName 上传/下载的目标盘名
        UpL_FilePath 上传文件路径
        DownL_FilePath 下载文件路径
        '''
        self.DriveName = DriveName
        self.UpL_FilePath = UpL_FilePath
        self.DownL_FilePath = DownL_FilePath

    def UpLoad(self):
        '''
        上传文件
        '''
        if self.DriveName == None or self.UpL_FilePath == None:
            st.warning('请输入上传的目标盘名/上传的文件路径')
        else:
            try:
                photos = deta.Drive(self.DriveName)
                photos.put(self.UpL_FilePath.split('/')
                           [-1], path=self.UpL_FilePath)
                st.success('✌已上传')
            except:
                st.error(traceback.format_exc())

    @app.get("/download/{name}")
    def DownLoad(self):
        '''
        下载文件
        '''
        if self.DriveName == None or self.DownL_FilePath == None:
            st.warning('请输入下载的目标盘名/下载的文件名')
        else:
            try:
                photos = deta.Drive(self.DriveName)
                res = photos.get(self.DownL_FilePath)
                st.success('✌已获取')
                return StreamingResponse(res.iter_chunks(1024), media_type="image/%s" % self.DownL_FilePath.split('.')[-1])
            except:
                st.error(traceback.format_exc())


colL, colR = st.columns(2)
with colL:
    with st.form('下载'):
        DriveName_input = st.text_input('目标盘符')
        FileName_input = st.text_input('要下载的文件名')
        submitted = st.form_submit_button('下载')
        if submitted:
            try:
                a = Photo(DriveName=DriveName_input,
                          DownL_FilePath=FileName_input)
                a.DownLoad()
            except:
                st.error(traceback.format_exc())
with colR:
    with st.form('上传'):
        DriveName_input = st.text_input('目标盘符')
        Path_input = st.text_input('要上传的文件路径')
        submitted = st.form_submit_button('上传')
        if submitted:
            try:
                a = Photo(DriveName=DriveName_input, UpL_FilePath=Path_input)
                a.UpLoad()
            except:
                st.error(traceback.format_exc())
