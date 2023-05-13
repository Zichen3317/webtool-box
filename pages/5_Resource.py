# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/19
#           Version:
#             Description: 导航
# ==========================================
import traceback
import streamlit as st
from MOD import YuQue_API
from deta import Deta
st.set_page_config(
    page_title="梓宸の资源站",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# 试验版应用"
    })


deta = Deta(st.secrets["deta_key"])
# 链接数据库[软件推荐]
db_Software = deta.Base('WEBToolBOX-streamlit-Software')
# 获取数据库表头（字典形式）
Content_Data = db_Software.fetch().items

tab1, tab2 = st.tabs(['软件推荐', '后台'])

with tab1:
    try:
        st.markdown(Content_Data[0]['name'])
    except:
        st.error(traceback.format_exc())

with tab2:
    with st.expander('软件推荐'):
        with st.form('后台-Software'):
            Author_PASSWORD_New = st.text_input('权限密码')
            FC_Select = st.selectbox(
                '选择功能', ("刷新软件推荐页的文章缓存", "查看缓存数据库[软件推荐]状态"))
            submitted = st.form_submit_button('运行')
            if submitted:
                if Author_PASSWORD_New == st.secrets["author_password"]:
                    if FC_Select == '刷新软件推荐页的文章缓存':
                        # 链接语雀API
                        Token = st.secrets["YuQue_Token"]
                        YQ = YuQue_API.YuQue(
                            Token=Token, Namespace='zichen-cjyu8/docs', DOCName='zme546').GetDocDetail()
                        Content = """
# {title}  
##### 作者：{user_name}   
##### 更新时间：{updated_time}  
{content}""".format(title=YQ['title'],
                            user_name=YQ['user_name'],
                            updated_time=YQ['updated_time'],
                            content=YQ['content_md'])

                        if len(Content_Data) == 1:
                            st.info('正在刷新缓存: %s-%s' %
                                    (YQ['title'], YQ['user_name']))
                            result = db_Software.put({
                                "name": Content,
                                "hometown": YQ['title']
                            }, Content_Data[0]['key'])
                            st.success('✔刷新成功！')
                            st.balloons()

                        elif len(Content_Data) == 0:
                            st.info('缓存数据库为空,正在写入缓存: %s-%s' %
                                    (YQ['title'], YQ['user_name']))
                            result = db_Software.put({
                                "name": Content,
                                "hometown": YQ['title']
                            })
                            st.success('✔写入成功！')
                        else:
                            st.warning('缓存数据库异常！ \n当前数据库数据条数：%s' %
                                       len(Content_Data))
                    elif FC_Select == '查看缓存数据库[软件推荐]状态':
                        st.metric('数据库数据数', len(Content_Data))
                else:
                    st.error('权限密码错误×')
