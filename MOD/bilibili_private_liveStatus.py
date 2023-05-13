# author： Zichen
# date: 2021-02-06
# instruction： 通过cookie获取自己关注的主播的开播信息

# 导入库
from urllib import request
import json
Version = '0.1'

# 用requests库的get()方法简明地获取网页信息。第一个函数返回一个网页内容---r.text.


def GetData(cookie):
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/w_live_users?size=10"  # 请求的url
    headers = {  # 请求的头部
        "origin": "https://t.bilibili.com",
        "referer": "https: // t.bilibili.com /",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
        "cookie": "%s" % cookie,
        "Host": "api.vc.bilibili.com"
    }

    req = request.Request(url=url, headers=headers)  # GET无data项
    res = request.urlopen(req)
    res = str(res.read(), encoding='utf-8')  # 将返回的bytes类型转为str类型
    data = json.loads(res)  # 如果是json/dict类型,这一步可以转为dict类型,前提是从str转
    # 用来最后输入st.table用以显示的字典
    DATA_Dict = {
    }
    # 用来存储各类数据，最后整合到DATA_Dict
    bili_private_title = []
    bili_private_url = []
    bili_private_name = []
    bili_private_uid = []
    for i in data.get('data').get('items'):
        bili_private_title.append(i['title'])
        bili_private_url.append(i['link'])
        bili_private_name.append(i['uname'])
        bili_private_uid.append(i['uid'])
    DATA_Dict['name'] = bili_private_name
    DATA_Dict['uid'] = bili_private_uid
    DATA_Dict['title'] = bili_private_title
    DATA_Dict['url'] = bili_private_url

    return DATA_Dict  # 返回小字典data
