# -*- coding: utf-8 -*-
# @Time : 2019/12/15 12:26
# @Author : Syu
import psutil
import requests
from lxml import etree


def unicom_login(username, password, login_out=False):
    """
    广东联通校园宽带登录
    :param username: 账号
    :param password: 密码
    :param login_out: 是否下线该账号
    :return:
    """
    response_info = requests.get("http://2.2.2.2", timeout=3)
    redit_list = response_info.history  # 获取联通重定向历史信息
    baspushurl = redit_list[len(redit_list)-1].headers["location"]  # 获取重定向url
    ip = baspushurl.split("&")[0].split("=")[1]  # 获取内网ip
    print(ip)
    url = 'http://portal.gd165.com/login.do'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/"
                  "signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "portal.gd165.com",
        "Origin": "http://portal.gd165.com",
        "Referer": "http://portal.gd165.com/index.do",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904"
                      ".108 Safari/537.36"
    }
    data = {
        "loginpage": "gd/campus/login.jsp",
        "onlinepage": "gd/campus/online.jsp",
        "accountsuffixname": "@16900.gd",
        "pagetype": "0",
        "macauth": "0",
        "accountvalid": "1800",
        "customerId": "001",
        "customerName": "campus",
        "basName": "120.80.172.172",
        "basPushUrl": baspushurl,
        "attrName": "ssid",
        "attrValue": "[capus.gz]",
        "wlanuserip": ip,
        "client_type": "xypttc",
        "basname": "120.80.172.172",
        "username": username,
        "password": password,
        "accountType": "fyhtc"
    }

    if login_out:  # 退出登录
        url = "http://portal.gd165.com/logout.do"
        headers["Referer"] = "http://portal.gd165.com/login.do"
        data["errormessage"] = "success"
        data['client_type'] = 'pz'
        data['useronline_id'] = '1'
        data['keepAliveTime'] = '1800000'
        data['isLogin'] = 'true'

    r = requests.post(url, headers=headers, data=data, timeout=5)
    soup = etree.HTML(r.text)
    result = soup.xpath('//*[@id="errormessage"]/@value')[0]
    if result == 'success':
        print("登录成功！")
    print(result)


if __name__ == '__main__':
    un = ""
    pw = ""
    unicom_login(un, pw, login_out=False)



