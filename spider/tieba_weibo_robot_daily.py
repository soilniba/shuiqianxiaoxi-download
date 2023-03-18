import urllib
import requests
import json
import time
import random
import math
import os
import tieba_weibo_robot_hour
from config import wx_robot_open, wx_robot_private, wx_robot_error, wx_robot_external, feishu_robot_private


def get_tieba(tieba_name):
    file_name = 'tieba_{}.json'.format(tieba_name)
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
    query_time = time.time() - 24 * 60 * 60    #上一天的时间
    local_time = time.localtime(query_time)
    yy_mm_dd = time.strftime("%Y_%m_%d", local_time)
    update_list = []
    for data_tid, data_info in  json_all.items():
        if (yy_mm_dd in data_info):
            # if data_info[yy_mm_dd] > data_info[yy_mm_dd]:   #只要比上个小时的回复量大就算热帖
            if data_info[yy_mm_dd] >= 10: #10条以上才配算热帖！
                update_list.append(data_info)
    if update_list:
        markdown_msg = '{}吧昨日热贴：\n'.format(tieba_name)
        def sort_fun(data_info):
            return data_info[yy_mm_dd]

        update_list.sort(key=sort_fun, reverse=True)
        # for data_info in update_list:
        for i in range(min(10, len(update_list))):
            data_info = update_list[i]
            markdown_msg += '{}条回复：{} https://tieba.baidu.com/{}\n'.format(data_info[yy_mm_dd], data_info['title'], data_info['title_href'])
            # print('{}条：{}'.format(data_info[yy_mm_dd], data_info['title']))
        print(markdown_msg)
        send_weibo_robot(markdown_msg)


# Request URL: https://picupload.weibo.com/interface/pic_upload.php?data=1&p=1&url=weibo.com/u/3086929951&markpos=1&logo=1&nick=@%E4%B8%93%E4%B8%9A%E4%B8%BE%E6%8A%A5%E5%B9%BF%E5%91%8A&marks=0&app=miniblog&s=json&pri=null&file_source=1

# data: 1
# p: 1
# url: weibo.com/u/3086929951
# markpos: 1
# logo: 1
# nick: @%E4%B8%93%E4%B8%9A%E4%B8%BE%E6%8A%A5%E5%B9%BF%E5%91%8A
# marks: 0
# app: miniblog
# s: json
# pri: null
# file_source: 1

# HTTP/1.1 200 OK
# Server: nginx/1.6.1
# Date: Sun, 18 Apr 2021 16:10:38 GMT
# Content-Type: application/json
# Transfer-Encoding: chunked
# Connection: keep-alive
# Access-Control-Allow-Origin: https://weibo.com
# Access-Control-Allow-Credentials: true
# LB_HEADER: ssl.33.wbpic.kxc.lb.sinanode.com

# POST /interface/pic_upload.php?data=1&p=1&url=weibo.com/u/3086929951&markpos=1&logo=1&nick=@%E4%B8%93%E4%B8%9A%E4%B8%BE%E6%8A%A5%E5%B9%BF%E5%91%8A&marks=0&app=miniblog&s=json&pri=null&file_source=1 HTTP/1.1
# Host: picupload.weibo.com
# Connection: keep-alive
# Content-Length: 408673
# sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
# sec-ch-ua-mobile: ?0
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36
# Content-Type: multipart/form-data
# Accept: */*
# Origin: https://weibo.com
# Sec-Fetch-Site: same-site
# Sec-Fetch-Mode: cors
# Sec-Fetch-Dest: empty
# Referer: https://weibo.com/
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# Cookie: SINAGLOBAL=6406279965343.804.1608098871543; login_sid_t=da3474730b256723703d5282051f1d9e; cross_origin_proto=SSL; _s_tentry=-; Apache=6456014565402.548.1618479567525; ULV=1618479567528:2:1:1:6456014565402.548.1618479567525:1608098871565; appkey=; SSOLoginState=1618552309; wvr=6; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhdJraewjFWsj0-zcj7VPAP5JpX5KMhUgL.Foe71hq4eo.4SK22dJLoI0qLxKBLBonL1KeLxKBLBonL1-2LxKBLBonLB.-LxKqL122LBK-LxK-LBo.LB.qLxK-L1K2L122t; SCF=Ag8CXZwE0_-v0vCtdVQ8soJE4wz01cLtd16Ce6D7nFomBZH9yjKip-5II7as1CoDigyUgML7GvjSIMornH9lNCY.; SUB=_2A25NeCioDeRhGeVO41QY8ifFzj2IHXVuDB1grDV8PUNbmtAKLWHGkW9NTXqw5UFlIRJZG197r2RPQdf6amW9krV8; ALF=1650297975; webim_unReadCount=%7B%22time%22%3A1618762245121%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D

# location: v6_content_home
# text: 111
# appkey: 
# style_type: 1
# pic_id: b7fed01fgy1gpoci74ngfj20u01hc4qp|b7fed01fgy1gpocj3yqitj20u00yekjl|b7fed01fgy1gpoclseaofj20n80ol49b|b7fed01fgy1gpoclsg2esj20me0ooqdr
# tid: 
# pdetail: 
# mid: 
# isReEdit: false
# gif_ids: 
# rank: 0
# rankid: 
# module: stissue
# pub_source: main_
# updata_img_num: 4
# pub_type: dialog
# isPri: null
# _t: 0
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
def send_weibo_robot(markdown_msg):
    global formData
    formData['text'] = markdown_msg
    data = urllib.parse.urlencode(formData).encode("utf-8")
    weibo_post_url = 'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=' + str(math.ceil(time.time() * 1000))
    request = urllib.request.Request(weibo_post_url, headers = tieba_weibo_robot_hour.get_weibo_headers(), data = data)
    response = urllib.request.urlopen(request)
    print(response.url)
    html = response.read().decode('utf-8')
        # print(html.encode('utf-8').decode('unicode_escape'))
        # '{"code":"100002","msg":"","data":"https:\\/\\/weibo.com\\/login.php?url=https%3A%2F%2Fweibo.com"}'
        # {"code":"100001","msg":"相似内容，建议您三个小时后再发送哦！如需帮助，请<a target="_blank" href="https:\/\/kefu.weibo.com">联系客服<\/a>","data":{}}
    if html.find('"code"') != -1:
        text_msg = '出错啦！发不出帖子啦！小彦宏出警啦！d'
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