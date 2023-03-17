import urllib
import requests
import json
import time
import random
import math
import os
robot_open = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e012d034-7c19-4ee9-a713-9e674ec9ce34'
robot_private = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=36f924a9-4911-4c7f-aa36-900c01c44237'
robot_error = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a4973542-3002-4cab-b853-be6b815d4cfa'

def get_tieba(tieba_name):
    file_name = f'tieba_{tieba_name}.json'
    json_all = load_json(file_name)
    update_info(tieba_name, json_all)

def load_json(file_name):
    try:
        f = open(file_name, "r", encoding='utf-8')
    except IOError:
        return {}
    else:
        return json.load(f)

def update_info(tieba_name, json_all):
    query_time = time.time() - 60 * 60    #上一小时的时间
    local_time = time.localtime(query_time)
    yy_mm_dd_hh = time.strftime("%Y_%m_%d_%H", local_time)
    update_list = []
    for data_tid, data_info in  json_all.items():
        if (yy_mm_dd_hh in data_info):
            # if data_info[yy_mm_dd_hh] > data_info[yy_mm_dd_hh_last]:   #只要比上个小时的回复量大就算热帖
            if data_info[yy_mm_dd_hh] >= 10: #10条以上才配算热帖！
                update_list.append(data_info)
    if update_list:
        hh = time.strftime("%H", local_time)
        markdown_msg = '{}吧{}点热贴：\n'.format(tieba_name, int(hh))
        def sort_fun(data_info):
            return data_info[yy_mm_dd_hh]

        update_list.sort(key=sort_fun, reverse=True)
        # for data_info in update_list:
        for i in range(min(5, len(update_list))):
            data_info = update_list[i]
            markdown_msg += '{}条回复：{} https://tieba.baidu.com/{}\n'.format(data_info[yy_mm_dd_hh], data_info['title'], data_info['title_href'])
            # print('{}条：{}'.format(data_info[yy_mm_dd], data_info['title']))
        print(markdown_msg)
        get_weibo_cookie()
        send_weibo_robot(markdown_msg)

cookie_file_name = 'sina_cookie_sub.txt'

def read_file_text(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            text = f.read()
            f.close()
            return text
    else:
        return ''

def get_weibo_cookie():
    data = urllib.parse.urlencode(formData).encode("utf-8")
    weibo_post_url = 'https://weibo.com/u/3086929951/home?wvr=5'
    request = urllib.request.Request(weibo_post_url, headers = get_weibo_headers(), data = data)
    response = urllib.request.urlopen(request)
    print(response.url)
    html = response.read().decode('utf-8')
    headerstr = response.getheaders()
    new_cookies = {}
    for k, v in headerstr:
        if "set-cookie" in k or "Set-Cookie" in k:
            if not v.find('deleted'):
                if v.find('SFC') or v.find('SUB') or v.find('SUBP'):
                    name, value = v.strip().split("=", 1)
                    new_cookies[name] = value
    if new_cookies:
        update_cookie(new_cookies)

def update_cookie(new_cookies):
    Cookie = read_file_text(cookie_file_name)
    cookie_text = ''
    for line in Cookie.split(";"):
        # print(line)
        if line.find("=") != -1:
            name,value = line.strip().split("=", 1)
            if name in new_cookies:
                value = new_cookies[name]
                print('cookie已更新', name, value)
            cookie_text = f'{cookie_text}{name}={value};'
    write_file_text(cookie_file_name, cookie_text)

def write_file_text(file_name, text):
    with open(file_name, "w") as f:
        f.write(text)
        f.close()

# Timestamp = (math.ceil(time.time() * 1000))
# cookie_before = 'SINAGLOBAL=6406279965343.804.1608098871543; login_sid_t=da3474730b256723703d5282051f1d9e; cross_origin_proto=SSL; _s_tentry=-; Apache=6456014565402.548.1618479567525; ULV=1618479567528:2:1:1:6456014565402.548.1618479567525:1608098871565; appkey=; SSOLoginState=1618552309; wvr=6; wb_view_log_3086929951=2560*14401; wb_timefeed_3086929951=1; ALF=1650204114; SCF=Ap6MjlPkuLaQ5RSwrKf-NP3OezWwAp8C7VIsilhQu0ypjVZEE5-o7f82oP-UO3MTV0wTx4PQoGub6KC01A7Qq0I.; '
# Cookie = cookie_before + read_file_text(cookie_file_name)
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhdJraewjFWsj0-zcj7VPAP5JpX5KMhUgL.Foe71hq4eo.4SK22dJLoI0qLxKBLBonL1KeLxKBLBonL1-2LxKBLBonLB.-LxKqL122LBK-LxK-LBo.LB.qLxK-L1K2L122t;
# Cookie = Cookie + '_2A25NfpoCDeRhGeVO41QY8ifFzj2IHXVuDYzKrDV_PUNbm9AKLXenkW9NTXqw5T0KmO1CcNL9WEMm8-G5BlB8Ft19'
weibo_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    # 'Cookie': Cookie,
    'referer': 'https://weibo.com/u/3086929951/home?wvr=5',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'method': 'POST',
    'x-requested-with': 'XMLHttpRequest',
}
formData = {
    'location': 'v6_content_home',
    'text': 'test',
    'appkey': '',
    'style_type': '1',
    'pic_id': '',
    'tid': '',
    'pdetail': '',
    'mid': '',
    'isReEdit': 'false',
    'rank': '0',
    'rankid': '',
    'module': 'stissue',
    'pub_source': 'main_',
    'pub_type': 'dialog',
    'isPri': '0',
    '_t': '0',
}

def get_weibo_headers():
    global weibo_headers
    Cookie = read_file_text(cookie_file_name)
    weibo_headers['Cookie'] = Cookie
    return weibo_headers

def send_weibo_robot(markdown_msg):
    global formData
    formData['text'] = markdown_msg
    data = urllib.parse.urlencode(formData).encode("utf-8")
    weibo_post_url = 'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=' + str(math.ceil(time.time() * 1000))
    request = urllib.request.Request(weibo_post_url, headers = get_weibo_headers(), data = data)
    response = urllib.request.urlopen(request)
    print(response.url)
    html = response.read().decode('utf-8')
        # print(html.encode('utf-8').decode('unicode_escape'))
        # '{"code":"100002","msg":"","data":"https:\\/\\/weibo.com\\/login.php?url=https%3A%2F%2Fweibo.com"}'
        # {"code":"100001","msg":"相似内容，建议您三个小时后再发送哦！如需帮助，请<a target="_blank" href="https:\/\/kefu.weibo.com">联系客服<\/a>","data":{}}
    if html.find('"code"') != -1:
        text_msg = '出错啦！发不出帖子啦！小彦宏出警啦！h'
        text_msg = f"{text_msg}\n{html.encode('utf-8').decode('unicode_escape')}"
        mentioned_list = [ 'wangchang@wangyuan.com' ]
        send_wx_robot(robot_error, text_msg, mentioned_list)
        print(text_msg)

def send_wx_robot(robot_url, content_msg, mentioned_list = None):
    headers = {
        'Content-Type': 'application/json',
    }
    if mentioned_list:
        data_table = {
            "msgtype": "text", 
            "text": { "content": content_msg, "mentioned_list": mentioned_list }
        }
    else:
        data_table = {
            "msgtype": "markdown", 
            "markdown": { "content": content_msg }
        }
    data = json.dumps(data_table)
    response = requests.post(robot_url, headers=headers, data=data)

def main():
    get_tieba('剑网3')

if __name__ == "__main__":
    main()