import json


def get_common_headers(cookies):
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "client-version": "v2.46.7",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://weibo.com/u/5266778656",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "server-version": "v2024.08.30.1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "x-requested-with": "XMLHttpRequest",
        "x-xsrf-token": cookies["XSRF-TOKEN"]
    }

def get_html_headers():
    return {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://weibo.com/tv/home",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

def trans_cookies(cookies_str):
    ck = {i.split('=')[0]: '='.join(i.split('=')[1:]) for i in cookies_str.split('; ')}
    return ck

if __name__ == '__main__':
    cookies_str = r'SCF=Anw5unmXGv7Tj6t7PbmvNhMdWZ9Yr7WmreQRFne7gnyOFrGSKkRNYbe1I6AXsA9AQiNZCZqlPqhNX0_JWzKHo2Q.; SUB=_2A25KliLXDeRhGeNP6VMY-SbFyDmIHXVp6jofrDV8PUNbmtANLUT7kW9NTrOGPDNNtHyeh5TQisnuhT83OKQsGNJ1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFAoaDvic4uvBz-E5c_5gfw5NHD95QfeKzp1K.R1KefWs4DqcjQICH8SbHW1C-41FH8SCHWxF-4eFH8SC-4eCHFeEH8SE-4BC-RSsfyd7tt; ALF=02_1740234631; WBPSESS=qVtvXfM6Pp6_zHT86UWMDdEsQz56uvZQsbWqIj8CStEKzzY-CxbwhCQiYqcA4M4D1diFRNMAnSjXJcAI5JxPCtRV0JuljYtPI6RvxrfA7UDs4COQ-sYv7XgTaWPCr4xLWFC0wGz009EIN7aTbEKjzA=='
    cookies = trans_cookies(cookies_str)
    print(json.dumps(cookies, ensure_ascii=False))