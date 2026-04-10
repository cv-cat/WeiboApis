import time
import json
import requests
from apis.weibo_apis import WeiboApis
from utils.weibo_creator_utils import generate_upload_image_media_headers, generate_upload_image_media_params, \
    generate_session_id, get_form_headers, generate_upload_video_media_headers, generate_upload_video_media_params, \
    generate_video_check_headers, generate_video_output_headers, get_post_image_headers, get_post_video_headers
from utils.weibo_utils import trans_cookies
from loguru import logger
class WeiboCreaterApis():

    def __init__(self):
        self.webApi = WeiboApis()
        self.base_url = ""

    def video_init(self, file, cookies_str):
        cookies = trans_cookies(cookies_str)
        t = str(int(time.time()))
        token = cookies['XSRF-TOKEN'] if 'XSRF-TOKEN' in cookies else ''
        headers = get_form_headers(t, token)
        url = "https://fileplatform.api.weibo.com/2/fileplatform/init.json"
        size = len(file)
        params = {
            "source": "339644097",
            "size": size,
            "name": "video.mp4",
            "type": "video",
            "client": "web",
        }
        session_id = generate_session_id(size, "video.mp4")
        params['session_id'] = session_id
        data = '--2067456weiboPro' + t + '\r\nContent-Disposition: form-data; name="biz_file"\r\n\r\n{"mediaprops":"{\\"screenshot\\":1}"}\r\n--2067456weiboPro' + t + '--\r\n'
        response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)
        res_json = response.json()
        return res_json

    def upload_image_file(self, uid, nick, file, cookies_str):
        url = 'https://picupload.weibo.com/interface/upload.php'
        cookies = trans_cookies(cookies_str)
        headers = generate_upload_image_media_headers()
        params = generate_upload_image_media_params(uid, nick, file)
        response = requests.post(url + '?' + params, cookies=cookies, headers=headers, data=file)
        res_text = response.text
        res_json = json.loads(res_text)
        return res_json


    def upload_video_file(self, upload_id, media_id, file, auth, cookies_str):
        url = 'https://up.video.weibocdn.com/2/fileplatform/upload.json'
        cookies = trans_cookies(cookies_str)
        headers = generate_upload_video_media_headers(len(file), auth)
        params = generate_upload_video_media_params(upload_id, media_id, file)
        response = requests.post(url + '?' + params, cookies=cookies, headers=headers, data=file)
        res_text = response.text
        res_json = json.loads(res_text)
        return res_json

    def video_check(self, upload_id, media_id, file_size, auth, cookies_str):
        cookies = trans_cookies(cookies_str)
        headers = generate_video_check_headers(auth)
        url = "https://fileplatform.api.weibo.com/2/fileplatform/check.json"
        data = {
            "source": "339644097",
            "upload_id": str(upload_id),
            "media_id": str(media_id),
            "upload_protocol": "binary",
            "count": "1",
            "action": "finish",
            "size": str(file_size),
            "client": "web",
            "status": ""
        }
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        res_json = response.json()
        return res_json

    def video_output(self, media_id,cookies_str):
        headers = generate_video_output_headers()
        cookies = trans_cookies(cookies_str)
        url = "https://weibo.com/ajax/multimedia/output"
        params = {
            "source": "339644097",
            "ids": media_id,
            "labels": "screenshot"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        res_json = response.json()
        return res_json

    def post_weibo(self, noteInfo, cookies_str):
        uid, nick = weiboCreaterApis.webApi.get_self_info(cookies_str)
        cookies = trans_cookies(cookies_str)
        token = cookies['XSRF-TOKEN'] if 'XSRF-TOKEN' in cookies else ''
        url = "https://weibo.com/ajax/statuses/update"
        if noteInfo['media_type'] == 'image':
            headers = get_post_image_headers(token)
            pic_id = []
            for image in noteInfo['images']:
                res_json = weiboCreaterApis.upload_image_file(uid, nick, image, cookies_str)
                pic_id.append({"type":  "image/jpeg", "pid": res_json['pic']['pid']})
            pic_id = json.dumps(pic_id)
            data = {
                "content": noteInfo['desc'],
                "visible": noteInfo['type'],
                "vote": "",
                "media": "",
                "pic_id": pic_id
            }
            for topic in noteInfo['topics']:
                data['content'] += f" #{topic}# "
            if noteInfo['location']:
                data['content'] += f" #{noteInfo['location']}[地点]#"
            response = requests.post(url, headers=headers, cookies=cookies, data=data)
            res_json = response.json()
            return res_json
        else:
            headers = get_post_video_headers(len(noteInfo['video']))
            res_json = weiboCreaterApis.video_init(noteInfo['video'], cookies_str)
            logger.info(f'1. video_init: {res_json}')
            if 'error' in res_json and 'user need identity authentication' == res_json['error']:
                logger.error('用户需要身份验证')
                return res_json
            upload_id, media_id, auth = res_json['upload_id'], res_json['media_id'], res_json['auth']
            res_json = weiboCreaterApis.upload_video_file(upload_id, media_id, noteInfo['video'], auth, cookies_str)
            logger.info(f'2. upload_video_file: {res_json}')
            res_json = weiboCreaterApis.video_check(upload_id, media_id, len(noteInfo['video']), auth, cookies_str)
            logger.info(f'3. video_check: {res_json}')
            while True:
                res_json = weiboCreaterApis.video_output(media_id, cookies_str)
                logger.info(f'4. video_output: {res_json}')
                if len(res_json['data'].keys()) > 0:
                    break
                time.sleep(2)
            url = "https://weibo.com/ajax/statuses/update"
            media = {
                'titles': [
                    {'title': '', 'default': 'true'}
                ],
                'covers': [{'url': ''}],
                'free_duration': {'start': 0, 'end': 30},
                'type': 'video',
                'media_id': media_id,
                'resource': {
                    'video_down': 1
                },
                'homemade': {
                    'channel_ids': [''],
                    'type': 0
                },
                'approval_reprint': '1'
            }
            data = {
                "content": noteInfo['desc'],
                "visible": noteInfo['type'],
                "vote": "",
                "media": json.dumps(media)
            }
            for topic in noteInfo['topics']:
                data['content'] += f" #{topic}# "
            if noteInfo['location']:
                data['content'] += f" #{noteInfo['location']}[地点]#"
            response = requests.post(url, headers=headers, cookies=cookies, data=data)

            res_json = response.json()
            return res_json

if __name__ == '__main__':
    weiboCreaterApis = WeiboCreaterApis()
    cookies_str = r'SCF=Au_GyJ8iteBAfwdVEZ_cTzHjL13gtYJnx3ir5oYS4KWlAYwEX650ITNv_jbaVQSvEH0ObyvpU12X-jeywQtAlkE.; XSRF-TOKEN=mJR785WNTS3b4Sj-1LnfASbv; ALF=1742442718; SUB=_2A25KsHOODeRhGeFH61cU8CzLzTqIHXVpzIlGrDV8PUJbkNANLVj7kW1NeDzyIFo3rwxRbOidrQdH5oseW2-okybD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFoWb6hF8xRil7mObi0Syxr5JpX5KMhUgL.FoM4eh-fehzNSoq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1K5fSK5ES0qc; WBPSESS=F-g56V5WRtN66TC4al6V9tfDALQepO3wdKzNdX8UFRN0yUFWC87tjsobYxaila_lirV58SgfvK63GmHqfqQCGQQ5dL2E40TzSWzvIk-dkv6xi7aqXdJdzVTe4QMvPX5_-8ULgZail3vseXzpYKojog=='
    noteInfos = [
        {
            # 描述
            "desc": "111222",
            # 设置地点 "河海大学"
            "location": '北京',
            # 0:公开 1:仅自己可见 6:朋友圈可见 10:粉丝可见
            "type": "1",
            "media_type": "image",
            # 设置话题
            "topics": ["雀魂", "麻将"],
            # 图片路径 最多15张
            "images": [
                open(r"D:/Desktop/Snipaste_2025-01-14_14-53-27.jpg", 'rb').read(),
                open(r"D:/Desktop/Snipaste_2025-01-14_14-53-27.jpg", 'rb').read(),
            ],
        },
        {
            "title": "222111",
            "desc": "222",
            "location": '南京',
            "topics": ["南京"],
            "type": "1",
            "media_type": "video",
            "video": open(r"D:\data\Videos\2024-05-02 21-14-45.mkv", 'rb').read(),
            # "video": open(r"D:\data\Videos\2024-11-13 18-09-01.mp4", 'rb').read(),
        }
    ]
    for noteInfo in noteInfos:
        res = weiboCreaterApis.post_weibo(noteInfo, cookies_str)
        logger.info(f'发布结果: {res}')

