import os
import re
import bs4
import time
import json

import pandas as pd
import requests
from utils.WeiboUtils import get_common_headers, trans_cookies, get_html_headers


class WeiboApis():

    def __init__(self):
        self.base_url = "https://weibo.com"


    def get_self_info(self, cookies_str):
        cookies = trans_cookies(cookies_str)
        headers = get_html_headers()
        url = "https://weibo.com/"
        response = requests.get(url, headers=headers, cookies=cookies)
        res_text = response.text
        user_info = re.findall(r'try\{window\.\$CONFIG = (.*?);}catch\(e\)\{window\.\$CONFIG', res_text)[0]
        user_info = json.loads(user_info)
        uid = user_info['user']['id']
        nick = user_info['user']['watermark']['nick']
        return str(uid), nick

    """
        获取用户信息
        :param userId: 用户id
        :param cookies_str: cookies
    """
    def getUserInfo(self, userId: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = "成功"
        res_json = None
        try:
            api = "/ajax/profile/info"
            params = {
                "uid": userId
            }
            cookies = trans_cookies(cookies_str)
            headers = get_common_headers(cookies)
            response = requests.get(self.base_url + api, headers=headers, cookies=cookies, params=params)
            res_json = response.json()
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    def getUserPosted(self, userId: str, page: str, since_id: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = "成功"
        res_json = None
        try:
            api = "/ajax/statuses/mymblog"
            params = {
                "uid": userId,
                "page": page,
                "feature": "0"
            }
            if since_id:
                params["since_id"] = since_id
            cookies = trans_cookies(cookies_str)
            headers = get_common_headers(cookies)
            response = requests.get(self.base_url + api, headers=headers, cookies=cookies, params=params)
            res_json = response.json()
        except Exception as e:
            print(f'爬取失败: {e}')
            success = False
            msg = str(e)
        return success, msg, res_json


    def getWordComments(self, userId, mid, cookies_str: str, proxies: dict = None):
        success = True
        msg = "成功"
        res_json = None
        try:
            url = "https://weibo.com/ajax/statuses/buildComments"
            params = {
                "is_reload": "1",
                "id": mid,
                "is_show_bulletin": "2",
                "is_mix": "0",
                "count": "10",
                "uid": userId,
                "fetch_level": "0",
                "locale": "zh-CN"
            }
            cookies = trans_cookies(cookies_str)
            headers = get_common_headers(cookies)
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            res_json = response.json()
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json


    def getWorkInfo(self, url: str, cookies_str: str, proxies: dict = None):
        success = True
        msg = "成功"
        res_json = None
        try:
            cookies = trans_cookies(cookies_str)
            headers = get_common_headers(cookies)
            response = requests.get(url, headers=headers, cookies=cookies)
            res_text = response.text
            res_text = re.findall(r'window\.\$CONFIG = (.*?);}catch\(e\)\{window\.\$CONFIG = \{\};}', res_text)[0]
            res_json = json.loads(res_text)
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json


    def searchSome(self, query: str, page, cookies_str: str, proxies: dict = None):
        success = True
        msg = "成功"
        res_json = None
        try:
            url = "https://s.weibo.com/weibo"
            params = {
                "q": query,
                "page": page
            }
            cookies = trans_cookies(cookies_str)
            headers = get_common_headers(cookies)
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            res_text = response.text
            # soup = bs4.BeautifulSoup(res_text, "html.parser")
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    def get_user_all_posted(self, user_url, cookies_str):
        since_id = ""
        res = []
        userId = user_url.split("/")[-1].split("?")[0]
        page = 1
        while True:
            success, msg, (res_json, r) = weiboApis.getUserPosted(userId, str(page), since_id, cookies_str)
            if not success:
                print(f'爬取用户 {user_url} 失败: {msg}')
                break
            since_id = res_json["data"]["since_id"] if "since_id" in res_json["data"] else ""
            page += 1
            res.extend(r)
            if not since_id:
                break
        return res


if __name__ == '__main__':
    weiboApis = WeiboApis()
    cookies_str = r'SCF=Ajh4L8OBQ-tXJiKUGE_lmfHysYXGMFk4Mp2mHGU4gB22MEEsudmDJJFKSMGGsy5LIoW1iBelXwmf4PpptNOUFkE.; SINAGLOBAL=3679216302677.1196.1731747701452; ULV=1731747701508:1:1:1:3679216302677.1196.1731747701452:; ALF=1735373084; SUB=_2A25KTFRMDeRhGeNP6VMY-SbFyDmIHXVpIOmErDV8PUJbkNANLVDekW1NTrOGPAbOwoEHvcMPfedhrZw9O9BVqHPq; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFAoaDvic4uvBz-E5c_5gfw5JpX5KMhUgL.Fo-peo241Kn4e0-2dJLoIEyDi--ci-24iK.Ri--fi-82iK.7i--fiK.pi-z0i--NiKLWiKnXdg8a; WBPSESS=qVtvXfM6Pp6_zHT86UWMDdEsQz56uvZQsbWqIj8CStEKzzY-CxbwhCQiYqcA4M4Dmf4ga5-XORwmsO465h4TSTgp9n6tc1G4ILkRf2TfHfWGrrNbDK7-vqB6Tsx-z1tR7EvZamFT8S1YgJJzHztj_w==; XSRF-TOKEN=YUogRQgUmzxs_2kMMcdKgKMk'
    userId = "5266778656"
    # success, msg, res_json = weiboApis.getUserInfo(userId, cookies_str)
    # print(success, msg, res_json)

    # since_id = ""
    # success, msg, res_json = weiboApis.getUserPosted(userId, since_id, cookies_str)
    # print(success, msg, json.dumps(res_json, ensure_ascii=False))
    # since_id = res_json["data"]["since_id"]
    # success, msg, res_json = weiboApis.getUserPosted(userId, since_id, cookies_str)
    # print(success, msg, res_json)

    # mblogid = "OuIv3hbiw"
    # mid = 5073209014095008
    # work_url = f'https://weibo.com/5266778656/{mblogid}'
    # success, msg, res_json = weiboApis.getWorkInfo(work_url, cookies_str)
    # print(success, msg, res_json)
    #
    # success, msg, res_json = weiboApis.getWordComments(userId, mid, cookies_str)
    # print(success, msg, res_json)

    user_url = r'https://weibo.com/u/7954288827'
    weiboApis.spider_one(user_url, cookies_str)
