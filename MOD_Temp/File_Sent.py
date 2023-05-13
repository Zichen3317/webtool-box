# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/16
#           Version:
#             Description: 只是用来存代码的
# ==========================================
with st.expander("发送文件→本地终端（仅供本地服务器使用）"):
    with st.form('发送文件'):

        uploaded_files = st.file_uploader("选择文件", accept_multiple_files=True)

        submitted_file = st.form_submit_button("发送")

        # 直接处理成自动识别单个/多个文件进行智能上传
        if submitted_file:
            try:
                file_TIME = str(datetime.today()).split('.')[
                    0].replace(':', '-').replace(' ', '-')

                try:
                    os.mkdir('./SENT_File')
                except:
                    pass
                os.mkdir('./SENT_File/%s' % file_TIME)

                if len(uploaded_files) > 1:
                    files_start_num = 1
                    files_total_num = len(uploaded_files)
                    FILE_Upload_Progress = st.progress(0)
                    st.info('文件上传中...')
                    for uploaded_file in uploaded_files:
                        bytes_data = uploaded_file.getvalue()
                        with open('./SENT_File/%s/%s' % (file_TIME, uploaded_file.name), 'wb') as f:
                            f.write(bytes_data)

                        # 上传进度条
                        FILE_Upload_Progress.progress(
                            round(files_start_num/files_total_num, 1))
                        files_start_num += 1
                    st.success('文件上传完成✓')
                elif len(uploaded_files) != 0:
                    bytes_data = uploaded_files[0].getvalue()
                    with open('./SENT_File/%s/%s' % (file_TIME, uploaded_files[0].name), 'wb') as f:
                        f.write(bytes_data)
                    st.success('文件上传完成✓')

            except:
                st.error(traceback.format_exc())
