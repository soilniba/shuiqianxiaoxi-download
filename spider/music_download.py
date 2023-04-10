from urllib.parse import urlparse, parse_qs
import requests

url = 'https://web.bxyuer.com/bixin-singer-annual-2023-s1/detailout/1680509413301?transferCode=30bab3e42148297b978f556ad88a0abb&singerUid=203390028547274622&shareUid=212100576408934029'

def get_singer(url):
    # 解析URL
    parsed_url = urlparse(url)

    # 获取参数
    query_params = parse_qs(parsed_url.query)

    # 获取shareSinger和singerUid
    share_singer = query_params.get('shareUid', [None])[0]
    singer_uid = query_params.get('singerUid', [None])[0]
    return share_singer, singer_uid

def get_audio_info(share_singer, singer_uid):
    url = 'https://gateway.bxyuer.com/singer/outside/singerDetail'
    payload = {
        "singerUid": singer_uid,
        "shareSinger": share_singer,
        "seasonId": 9,
        "prev": 1
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        json = response.json() 
        return json['result']['audioUrl']
    else:
        print("请求失败，状态码：", response.status_code)


share_singer, singer_uid = get_singer(url)
music_url = get_audio_info(share_singer, singer_uid)
print(music_url)

