import hashlib
import time
import urllib


def get_file_md5(file):
    """Calculate MD5 hash of file."""
    return hashlib.md5(file).hexdigest()


def get_file_cs(data):
    """Calculate CRC32 checksum of binary data."""
    # Complete CRC32 lookup table
    crc_table = [
        0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3,
        0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988, 0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91,
        0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE, 0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7,
        0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC, 0x14015C4F, 0x63066CD9, 0xFA0F3D63, 0x8D080DF5,
        0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172, 0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B,
        0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940, 0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59,
        0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116, 0x21B4F4B5, 0x56B3C423, 0xCFBA9599, 0xB8BDA50F,
        0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924, 0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D,
        0x76DC4190, 0x01DB7106, 0x98D220BC, 0xEFD5102A, 0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433,
        0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818, 0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01,
        0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E, 0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457,
        0x65B0D9C6, 0x12B7E950, 0x8BBEB8EA, 0xFCB9887C, 0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65,
        0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2, 0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB,
        0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0, 0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9,
        0x5005713C, 0x270241AA, 0xBE0B1010, 0xC90C2086, 0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F,
        0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4, 0x59B33D17, 0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD,
        0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A, 0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683,
        0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8, 0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1,
        0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE, 0xF762575D, 0x806567CB, 0x196C3671, 0x6E6B06E7,
        0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC, 0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5,
        0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252, 0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B,
        0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60, 0xDF60EFC3, 0xA867DF55, 0x316E8EEF, 0x4669BE79,
        0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236, 0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F,
        0xC5BA3BBE, 0xB2BD0B28, 0x2BB45A92, 0x5CB36A04, 0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D,
        0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A, 0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713,
        0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38, 0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21,
        0x86D3D2D4, 0xF1D4E242, 0x68DDB3F8, 0x1FDA836E, 0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777,
        0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C, 0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45,
        0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2, 0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB,
        0xAED16A4A, 0xD9D65ADC, 0x40DF0B66, 0x37D83BF0, 0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9,
        0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6, 0xBAD03605, 0xCDD70693, 0x54DE5729, 0x23D967BF,
        0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94, 0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D
    ]

    crc = 0xFFFFFFFF
    for byte in data:
        crc = (crc >> 8) ^ crc_table[(crc & 0xFF) ^ byte]
    return crc ^ 0xFFFFFFFF


def get_file_binary_string(file):
    """Read file in binary mode."""
    return file


def generate_params(file):
    """Generate both CS and MD5 hash for a file."""
    if isinstance(file, str):
        binary_data = get_file_binary_string(file)
        cs = get_file_cs(binary_data)
        md5 = get_file_md5(file)
        file_size = len(binary_data)
    else:
        cs = get_file_cs(file)
        md5 = get_file_md5(file)
        file_size = len(file)
    return {
        'cs': cs,
        'md5': md5,
        'file_size': file_size
    }

def generate_session_id(file_size, file_name):
    t1 = int(time.time() * 1000)
    t2 = int(time.time())
    s = f'{t1}|{file_size}|{file_name}|video|{t2}'
    md5_hash = hashlib.md5(s.encode()).hexdigest()
    return md5_hash

def generate_upload_image_media_headers():
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/octet-stream',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'SCF=Ag7ghnvRb8_0TRgNk0ap7bMGRYiCeDcHIubKvxvyE_XCKv9re2zre1vdYWHDBMhmYztud-73EKtK0jLcdpz_zoY.; SUB=_2A25Klnf3DeRhGeNP6VMY-SbFyDmIHXVp6vU_rDV8PUNbmtANLVn6kW9NTrOGPJaEoGXUSlh7F40epwjlwmTNU8ve; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFAoaDvic4uvBz-E5c_5gfw5NHD95QfeKzp1K.R1KefWs4DqcjQICH8SbHW1C-41FH8SCHWxF-4eFH8SC-4eCHFeEH8SE-4BC-RSsfyd7tt; ALF=02_1740215463',
        'origin': 'https://weibo.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://weibo.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

def generate_upload_image_media_params(uid, nick, file_info):
    p = generate_params(file_info)
    params = {
        'file_source': '1',
        'cs': str(p['cs']),
        'ent': 'miniblog',
        'appid': '339644097',
        'uid': uid,
        'raw_md5': str(p['md5']),
        'ori': '1',
        'mpos': '1',
        'nick': nick,
        'pri': '0',
        'request_id': str(int(time.time() * 1000)),
        'file_size': str(p['file_size']),
    }
    return urllib.parse.urlencode(params)

def generate_video_check_headers(auth):
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://weibo.com",
        "Pragma": "no-cache",
        "Referer": "https://weibo.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "X-Up-Auth": auth,
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

def generate_video_output_headers():
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://weibo.com/upload/channel",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

def generate_upload_video_media_headers(file_size, auth):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-length': str(file_size),
        'content-type': 'application/octet-stream',
        'host': 'up.video.weibocdn.com',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'SCF=Ag7ghnvRb8_0TRgNk0ap7bMGRYiCeDcHIubKvxvyE_XCKv9re2zre1vdYWHDBMhmYztud-73EKtK0jLcdpz_zoY.; SUB=_2A25Klnf3DeRhGeNP6VMY-SbFyDmIHXVp6vU_rDV8PUNbmtANLVn6kW9NTrOGPJaEoGXUSlh7F40epwjlwmTNU8ve; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFAoaDvic4uvBz-E5c_5gfw5NHD95QfeKzp1K.R1KefWs4DqcjQICH8SbHW1C-41FH8SCHWxF-4eFH8SC-4eCHFeEH8SE-4BC-RSsfyd7tt; ALF=02_1740215463',
        'origin': 'https://weibo.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://weibo.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'x-up-auth': auth,
    }

def generate_upload_video_media_params(upload_id, media_id, file_info):
    p = generate_params(file_info)
    params = {
        'source': '339644097',
        'upload_id': str(upload_id),
        'media_id': str(media_id),
        'upload_protocol': 'binary',
        'type': 'video',
        'client': 'web',
        'check': str(p['md5']),
        'index': '0',
        'size': str(p['file_size']),
        'start_loc': '0',
        'count': '1',
    }
    return urllib.parse.urlencode(params)

def get_post_image_headers(token):
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "client-version": "v2.47.25",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://weibo.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://weibo.com/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "server-version": "v2025.01.23.1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "x-xsrf-token": token
    }

def get_post_video_headers(file_size):
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "client-version": "v2.47.25",
        "content-length": str(file_size),
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://weibo.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://weibo.com/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "server-version": "v2025.01.23.1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
def get_form_headers(t, token):
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": f"multipart/mixed; boundary=2067456weiboPro{t}",
        "Origin": "https://weibo.com",
        "Pragma": "no-cache",
        "Referer": "https://weibo.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

if __name__ == '__main__':
    file_path = 'D:/Desktop/Snipaste_2025-01-14_14-53-27.jpg'
    file_path = r"D:\data\Videos\1.mp4"
    with open(file_path, 'rb') as f:
        file_info = f.read()
    print(len(file_info))
    params = generate_params(file_info)
    print(params)


