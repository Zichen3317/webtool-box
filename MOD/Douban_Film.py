# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/19
#           Version:
#             Description: 爬取豆瓣正在上映电影讯息（汕头）
# ==========================================
# 由于整个程序的入口文件是Home.py,故在服务器上运行时需要从MOD包里导入HTML_crawler
# 而在本地只调试本py文件时，则是直接在同级目录中导入HTML_crawler
try:
    from MOD import HTML_crawler
except:
    import HTML_crawler
import pandas as pd


class Film:
    '''
    爬取豆瓣正在/即将上映电影列表
    '''

    def __init__(self, city='shantou'):
        self.url = 'https://movie.douban.com/cinema/nowplaying/%s/' % city
        self.DATA = HTML_crawler.GetData(self.url).GetHTMLDATA()

    def NowPlaying_GET_FILM(self):
        # 获取所有电影信息
        DATA_List = self.DATA.find('div', {'id': 'nowplaying'}).find('ul', {'class': 'lists'}).findAll(
            'li', {'class': 'list-item'})
        # 分别获取所需信息
        Film_Data = {}
        DATA_Title = []
        DATA_Score = []
        for i in DATA_List:
            DATA_Title.append(i['data-title'])
            score = i['data-score']
            if score != '0':
                DATA_Score.append(score)
            else:
                DATA_Score.append('暂无评分')
        Film_Data['片名'] = DATA_Title
        Film_Data['分数'] = DATA_Score
        Film_DataFrame = pd.DataFrame(Film_Data)
        return Film_DataFrame

    def Upcoming_GET_FILM(self):
        DATA_List = self.DATA.find('div', {'id': 'upcoming'}).find('ul', {'class': 'lists'}).findAll(
            'li', {'class': 'list-item'})
        DATA_ReleaseDate_List = self.DATA.find('div', {'id': 'upcoming'}).find('ul', {'class': 'lists'}).findAll(
            'li', {'class': 'release-date'})
        # 分别获取所需信息
        Film_Data = {}
        DATA_Title = []
        DATA_Actors = []
        DATA_ReleaseDate = []
        for i in DATA_List:
            DATA_Title.append(i['data-title'])
            DATA_Actors.append(i['data-actors'])

        for i in DATA_ReleaseDate_List:
            # <li class="release-date">06月24日上映</li> 像这样， i.name = li ,i.string = 06月24日上映, i['class'] = release-date
            DATA_ReleaseDate.append(
                str(i.string).replace(' ', '').replace('\n', '').replace('上映', ''))
        Film_Data['片名'] = DATA_Title
        Film_Data['领衔主演'] = DATA_Actors
        Film_Data['上映时间'] = DATA_ReleaseDate
        Film_DataFrame = pd.DataFrame(Film_Data)
        return Film_DataFrame

    def City_GET_DATA(self):
        City_Total = self.DATA.find(
            'div', {'class': 'cities-list-bd'}).findAll('a')
        City_DATA = {}
        for i in City_Total:
            City_DATA[str(i.string)] = str(i['uid'])
        return City_DATA
