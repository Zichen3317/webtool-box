# author： Zichen
# date(1.0): 2021-02-06
# Update(1.1)：2022-06-14
#vision: 1.1
# instruction：通过uid获取主播开播信息
# 导入库
from urllib import request
import json
Version = '0.1'

# 用requests库的get()方法简明地获取网页信息。第一个函数返回一个网页内容---r.text.


def GetLiveStatus(data):  # 获得小字典data中的直播状况
    LiveStatus = data.get('liveStatus')
    if LiveStatus == 0:
        return '未直播'
    elif LiveStatus == 1:
        return '正在直播'


def GetLive_title(data):  # 获得小字典data中的直播间标题
    Live_title = data.get('title')
    return(Live_title)


def GetLive_url(data):  # 获得小字典data中的直播间链接
    Live_url = data.get('url')
    return(Live_url)


def GetName_Mid(data):  # 获得大字典data中的UP名和uid
    Name = data.get('data').get('name')
    UID = str(data.get('data').get('mid'))
    NM_list = ['%s' % Name, '%s' % UID]
    return NM_list


def GetData(mid):
    url = "https://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp" % mid  # 请求的url
    headers = {  # 请求的头部
        'origin': "https://space.bilibili.com",
        'referer': "https://space.bilibili.com/",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
        'Host': "api.bilibili.com"
    }

    req = request.Request(url=url, headers=headers)  # GET无data项
    res = request.urlopen(req)
    res = str(res.read(), encoding='utf-8')  # 将返回的bytes类型转为str类型
    # 如果是json/dict类型,这一步可以转为dict类型,前提是从str转
    data = json.loads(res)
    # 详细的数据
    data_detail = data.get('data').get('live_room')
    # 2022/06/14 🧰 为减少主程序文件再次处理数据造成代码量过大，
    # 故将所有数据处理完毕后以列表形式一并返回
    # 返回字典数据顺序:
    # {
    #   直播状况,直播间标题,直播间链接,UP名和uid
    # }
    total_data = {'liveStatus': GetLiveStatus(data_detail),
                  'title': GetLive_title(data_detail),
                  'url': GetLive_url(data_detail),
                  'name': GetName_Mid(data)[0],
                  'uid': GetName_Mid(data)[1]}

    return total_data


def index():
    # 默认用于测试的列表
    Default = ['302145',
               '14897804',
               '11073',
               '7223194',
               '11253297',
               '282994',
               '7966',
               '617285',
               ]

    # 用来最后输入st.table用以显示的字典
    DATA_Dict = {
    }
    # 用来存储各类数据，最后整合到DATA_Dict
    bili_public_liveStatus = []
    bili_public_title = []
    bili_public_url = []
    bili_public_name = []
    bili_public_uid = []
    for i in Default:
        a = GetData(i)
        bili_public_liveStatus.append(a['liveStatus'])
        bili_public_title.append(a['title'])
        bili_public_url.append(a['url'])
        bili_public_name.append(a['name'])
        bili_public_uid.append(a['uid'])
    DATA_Dict['name'] = bili_public_name
    DATA_Dict['uid'] = bili_public_uid
    DATA_Dict['liveStatus'] = bili_public_liveStatus
    DATA_Dict['title'] = bili_public_title
    DATA_Dict['url'] = bili_public_url
    return DATA_Dict
