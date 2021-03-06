# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        ð§Mail: 1538185121@qq.com
#         âTime: 2022/06/16
#           Version:
#             Description: åæç« ç¨çè¾å©å·¥å·
# ==========================================
import traceback
from datetime import datetime
import streamlit as st
from deta import Deta
from MOD import PushDeer
import pytz
# ä¸»é¡µé¢è®¾ç½®
st.set_page_config(
    page_title="æ¢å®¸ã®åä½å·¥å·",
    page_icon="ð",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://gitee.com/ZiChen_3317/webtool-box',
        'Report a bug': "https://gitee.com/ZiChen_3317/webtool-box/issues",
        'About': "# è¯éªçåºç¨"
    })

# é¾æ¥æ°æ®åº
deta = Deta(st.secrets["deta_key"])
db = deta.Base('demo001-WEBToolBOX-streamlit-Article')
PushDeer_key = st.secrets['PushDeer_key']
# è·åæ°æ®åºæ°æ® [{}]
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
Tool_Version = '0.3'
st.markdown("## ðåä½å·¥å·ð\n *çæ¬å·:%s*" % Tool_Version)
tab1, tab2, tab3 = st.tabs(["ðåä½", "ðä¿®æ¹", "âå é¤"])
with tab1:
    st.markdown("### ðåä½")
    with st.form('æç« å¿è¦ä¿¡æ¯å½å¥'):
        Author_PASSWORD_New = st.text_input('æéå¯ç ')
        Article_Name = st.text_input('æç« åç§°')
        Article_Author = st.text_input('ä½è')
        Article_Content = st.text_area('æç« åå®¹')
        preview = st.form_submit_button('é¢è§ð')
        submitted = st.form_submit_button('åå¸æç« ')
        if submitted:
            if Author_PASSWORD_New == st.secrets["author_password"]:
                submitted_Time = str(datetime.now(pytz.timezone('Asia/Shanghai'))).split('.')[
                    0].split(' ')[0]
                try:
                    st.info('å¼å§åå¥ %s-%s' % (Article_Author, Article_Name))
                    result = db.put({
                        "name": "%s|%s-%s" % (submitted_Time, Article_Author, Article_Name),
                        "hometown": str(Article_Content)
                    })
                    st.success('âåå¥æåï¼')
                    st.balloons()
                    # æ¨éä¿¡æ¯
                    PushDeer.PushDeer_Sent(PushDeer_key, "[{Time}] - {Name} - å·²ä¸ä¼ ".format(
                        Time=str(datetime.now(pytz.timezone(
                            'Asia/Shanghai'))).split('.')[0],
                        Name="%s|%s-%s" % (submitted_Time,
                                           Article_Author, Article_Name)
                    ))
                except:
                    st.error(traceback.format_exc())
            else:
                st.warning("âæªè·åä¸ä¼ æéï¼è¯·æ£æ¥æéå¯ç æ¯å¦æ­£ç¡®ï¼")

with tab2:
    st.markdown("### ðä¿®æ¹")
    with st.form('éä¿®æ¹æç« æäº¤'):
        Author_PASSWORD_Modify = st.text_input('æéå¯ç ')
        Article_Select = st.selectbox(
            "æ°æ®åºæç« åè¡¨", Article_Dict.keys())
        Article_Modify_view = st.form_submit_button('æ¥ç')
        Article_Modify_Content = st.text_area(
            label='ä¿®æ¹åçæç« åå®¹', value='')

        Article_Modify_preview = st.form_submit_button('é¢è§')
        Article_Modify_submitted = st.form_submit_button('ä¿®æ¹')

        if Article_Modify_submitted:
            if Author_PASSWORD_Modify == st.secrets["author_password"]:
                Modify_Time = str(datetime.now(pytz.timezone('Asia/Shanghai'))).split('.')[
                    0].split(' ')[0]
                try:
                    # TIPï¼æç« åç§°æ ¼å¼ä¸º åå»ºæ¥æ|ä½è-æç« åï¼ä¸ä¼ ä¿®æ¹çæ¬åéè¦æåå»ºæ¥ææ¿æ¢æ
                    st.info('å¼å§ä¿®æ¹%s' %
                            Article_Select.split('|')[-1])
                    # ä¿®æ¹æ¶ééå¸¦ä¸ä¼ åæç« key
                    # æ³¨æå¨éå½åæ¶ï¼ç±äºåæç« åä¸­åå«äºæ¶é´ï¼æéè¦å°åæ¶é´åé¤åå å¥æ°æ¶é´
                    result = db.put({
                        "name": "%s|%s" % (Modify_Time, Article_Select.split('|')[-1]),
                        "hometown": '- *[ä¿®æ¹æ¶é´] %s* \n%s' % (Modify_Time, Article_Modify_Content)}, Article_Dict[Article_Select]['key'])
                    st.success('âä¿®æ¹æåï¼')
                    st.balloons()
                    # æ¨éä¿¡æ¯
                    PushDeer.PushDeer_Sent(PushDeer_key, "[{Time}] - {Name} - è¿è¡äºä¿®æ¹".format(
                        Time=str(datetime.now(pytz.timezone(
                            'Asia/Shanghai'))).split('.')[0],
                        Name="%s|%s" % (
                            Modify_Time, Article_Select.split('|')[-1])
                    ))
                except:
                    st.error(traceback.format_exc())
            else:
                st.warning("âæªè·åä¿®æ¹æéï¼è¯·æ£æ¥æéå¯ç æ¯å¦æ­£ç¡®ï¼")

# å é¤æç« æä½çªå£
with tab3:
    st.markdown("### âå é¤")
    with st.form('å é¤æå®æç« '):
        Author_PASSWORD_Delete = st.text_input('æéå¯ç ')
        # å¤éæ¡ï¼è¿ååè¡¨
        Article_MutiSelect = st.multiselect(
            "æ°æ®åºæç« åè¡¨", Article_Dict.keys())

        Article_Delete_preview = st.form_submit_button('é¢è§')
        Article_Delete_submitted = st.form_submit_button('å é¤')

        if Article_Delete_submitted:
            if Author_PASSWORD_Delete == st.secrets["author_password"]:
                try:
                    Delete_Message = ''
                    for i in Article_MutiSelect:
                        result = db.delete(Article_Dict[i]['key'])
                        Delete_Message = Delete_Message+'å·²å é¤:%s\n' % i
                    st.info(Delete_Message)
                    PushDeer.PushDeer_Sent(PushDeer_key, "[{Time}] - {Message} - å·²å é¤".format(
                        Time=str(datetime.now(pytz.timezone(
                            'Asia/Shanghai'))).split('.')[0],
                        Message=Delete_Message)
                    )

                except:
                    st.error(traceback.format_exc())
            else:
                st.warning("âæªè·åå é¤æéï¼è¯·æ£æ¥æéå¯ç æ¯å¦æ­£ç¡®ï¼")


# ä¸­é¨æ¯é¢è§çªå£ï¼éè¦æ¾å¨æå
with st.container():
    st.markdown("***")
    st.markdown("### ðé¢è§çé¢")

# åä½æ¶çæç« é¢è§
    if preview:
        preview_Time = str(datetime.now(pytz.timezone('Asia/Shanghai'))).split('.')[
            0].split(' ')[0]

        st.markdown('\n ## %s|%s-%s' %
                    (Article_Name, Article_Author, preview_Time))
        st.markdown(Article_Content)
# ä¿®æ¹æ¶çæç« é¢è§

    if Article_Modify_view:
        st.markdown("## ä¿®æ¹åæç« :")
        st.text("%s " %
                Article_Dict[Article_Select]['content'])
        st.markdown("***")
        st.markdown(' ## %s' % Article_Select)
        st.markdown(Article_Dict[Article_Select]['content'])
    if Article_Modify_preview:
        st.markdown(Article_Modify_Content)

# å é¤æ¶çæç« é¢è§
    if Article_Delete_preview:
        for i in Article_MutiSelect:
            with st.expander(i):
                st.markdown(Article_Dict[i]['content'])
