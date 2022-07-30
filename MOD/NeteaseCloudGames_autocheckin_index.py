import requests as r
import streamlit as st
Version = '0.1'


def Autocheckin(cookies):
    if cookies == "" or cookies == []:
        st.error('[网易云游戏自动签到]未设置cookie！')
    sign_url = 'https://n.cg.163.com/api/v2/sign-today'
    current = 'https://n.cg.163.com/api/v2/client-settings/@current'
    st.info('检测到{}个账号，即将开始签到！'.format(len(cookies)))
    success = []
    failure = []
    msg = []
    for i in cookies:
        cookie = i
        autherror = False
        signerror = False
        sign_return = None
        me = None
        try:
            me = getme(current, cookie)
        except:
            message = '第{}个账号验证失败！请检查Cookie是否过期！'.format(
                cookies.index(i) + 1)
            failure.append(cookie)
            msg.append(message)
            autherror = True

        if me.status_code != 200 and not autherror:
            message = '第{}个账号验证失败！请检查Cookie是否过期！'.format(
                cookies.index(i) + 1)
            failure.append(cookie)
            msg.append(message)
        elif me.status_code == 200:
            try:
                sign_return = signin(
                    sign_url, cookie)
            except:
                message = '第{}个账号签到失败，回显状态码为{}，具体错误信息如下：{}'.format(
                    cookies.index(i) + 1, sign_return.status_code, sign_return.text)
                failure.append(cookie)
                msg.append(message)
                signerror = True

            if sign_return.status_code == 200:
                message = '第{}个账号签到成功！'.format(cookies.index(i) + 1)
                success.append(cookie)
                msg.append(message)
            elif not signerror:
                message = '第{}个账号签到失败，回显状态码为{}，具体错误信息如下：{}'.format(
                    cookies.index(i) + 1, sign_return.status_code, sign_return.text)
                failure.append(cookie)
                msg.append(message)
    outputmsg = str(msg).replace("[", '').replace(
        ']', '').replace(',', '<br>').replace('\'', '')
    Mailinfomsg = '''
    =网易云游戏自动签到脚本=
    今日签到结果如下：
    ✅成功数量：{0}/{2}
    ❌失败数量：{1}/{2}
    具体情况如下：
    {3}

    '''.format(len(success), len(failure), len(cookies), outputmsg)
    return Mailinfomsg
    if (len(failure) != 0):
        st.error("[网易云游戏自动签到]脚本运行错误，具体请参见日志！")


def signin(url, cookie):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
        'Authorization': str(cookie),
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'n.cg.163.com',
        'Origin': 'https://cg.163.com',
        'Referer': 'https://cg.163.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Platform': '0'
    }

    result = r.post(url=url, headers=header)
    return result


def getme(url, cookie):
    header = {
        'Host': 'n.cg.163.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Platform': '0',
        'Authorization': str(cookie),
        'Origin': 'https://cg.163.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cg.163.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5'
    }
    result = r.get(url=url, headers=header)
    return result
