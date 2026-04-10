import re
import json
import requests
from utils.WeiboMobileUtils import get_search_headers, get_detail_headers

class WeiboMobileApis():

    def __init__(self):
        self.base_url = "https://weibo.com"


    def getWorkInfo(self, work_id: str):
        success = True
        msg = "成功"
        res_json = None
        try:
            url = f"https://m.weibo.cn/detail/{work_id}"
            headers = get_detail_headers()
            response = requests.get(url, headers=headers)
            res_text = response.text
            res_text = re.findall(r'var \$render_data = \[(.*?)]\[0\] \|\| \{\};\n  var __wb_performance_data=\{v:"v8",m:"mainsite",pwa:1,sw:0};', res_text, re.S)
            res_json = json.loads(res_text[0])

        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json


    def searchSome(self, query: str, page=1):
        success = True
        msg = "成功"
        res_json = None
        try:
            url = "https://m.weibo.cn/api/container/getIndex"
            params = {
                "containerid": f"100103type=1&q={query}",
                "page_type": "searchall",
                "page": str(page)
            }
            headers = get_search_headers()
            response = requests.get(url, headers=headers, params=params)
            res_json = response.json()
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json


if __name__ == '__main__':
    weiboMobileApis = WeiboMobileApis()
    success, msg, res_json = weiboMobileApis.searchSome("甄诚")
    for i in res_json["data"]["cards"]:
        try:
            detail = i["card_group"][0]["mblog"]
            work_id = detail["id"]
            print(work_id)
            success, msg, res_json = weiboMobileApis.getWorkInfo(work_id)
            print(success, msg, res_json)
        except:
            pass
