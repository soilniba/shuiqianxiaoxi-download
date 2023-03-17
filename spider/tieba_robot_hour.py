from bs4 import BeautifulSoup
import random
import json
import time
import requests
import os

wx_robot_open = 'e012d034-7c19-4ee9-a713-9e674ec9ce34'
wx_robot_private = '36f924a9-4911-4c7f-aa36-900c01c44237'
wx_robot_error = 'a4973542-3002-4cab-b853-be6b815d4cfa'
wx_robot_external = '274c2867-0698-4165-aabb-f02e0d60d4c0'
feishu_robot_private = 'af4ca118-394a-4b55-96b8-3c7beb2d18c7'

def get_tieba(tieba_name, robot_url, feishu_robot_key = False):
    file_name = f'tieba_{tieba_name}.json'
    json_all = load_json(file_name)
    update_info(tieba_name, json_all, robot_url, feishu_robot_key)

def load_json(file_name):
    try:
        f = open(file_name, "r", encoding='utf-8')
    except IOError:
        return {}
    else:
        return json.load(f)
flag_emoji_list = [
    '😕',
    '😟',
    '😮',
    '😲',
    '😳',
    '😨',
    '😰',
    '😖',
    '😣',
    '😞',
    '😓',
    '😭',
    '😱',
]
def update_info(tieba_name, json_all, robot_url, feishu_robot_key):
    query_time = time.time() - 60 * 60    #上一小时的时间
    local_time = time.localtime(query_time)
    yy_mm_dd_hh = time.strftime("%Y_%m_%d_%H", local_time)
    update_list = []
    for data_tid, data_info in  json_all.items():
        if (yy_mm_dd_hh in data_info):
            # if data_info[yy_mm_dd_hh] > data_info[yy_mm_dd_hh_last]:   #只要比上个小时的回复量大就算热帖
            if data_info[yy_mm_dd_hh] >= 5: #10条以上才配算热帖！
                update_list.append(data_info)
    if update_list:
        hh = time.strftime("%H", local_time)
        markdown_msg = '⏰{1}点👉<font color=\"info\">{0}吧</font>👈热贴：\n'.format(tieba_name, int(hh))
        feishu_msg = {"content": []}
        feishu_msg["title"] = '⏰{}点👉{}吧👈热贴：'.format(int(hh), tieba_name)
        def sort_fun(data_info):
            return data_info[yy_mm_dd_hh]

        update_list.sort(key=sort_fun, reverse=True)
        random_emoji_list = random.sample(flag_emoji_list, len(flag_emoji_list))
        # for data_info in update_list:
        for i in range(min(5, len(update_list))):
            data_info = update_list[i]
            emoji = '🚩'
            emoji = '🔥🔥' if i < 1 else random_emoji_list.pop()
            markdown_msg += '><font color=\"warning\">{0}</font>条回复：{3}[{1}](https://tieba.baidu.com{2})\n'.format(data_info[yy_mm_dd_hh], data_info['title'], data_info['title_href'], emoji)
            feishu_msg["content"].append([
                {
                    "tag": "text",
                    "text": '{}条回复：{}'.format(data_info[yy_mm_dd_hh], emoji)
                },
                {
                    "tag": "a",
                    "text": data_info['title'],
                    "href": 'https://tieba.baidu.com' + data_info['title_href']
                }
            ])
                    # print('{}条：{}'.format(data_info[yy_mm_dd], data_info['title']))
        print(markdown_msg)
        send_wx_robot(robot_url, markdown_msg)
        if feishu_robot_key != False:
            send_feishu_robot(feishu_robot_key, feishu_msg)

def send_wx_robot(robot_url, markdown_msg):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "msgtype": "markdown", 
        "markdown": { "content": markdown_msg },
    })
    response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_url, headers=headers, data=data)

def send_feishu_robot(feishu_robot_key, feishu_msg):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": feishu_msg
            }
        }
    })
    response = requests.post('https://open.feishu.cn/open-apis/bot/v2/hook/' + feishu_robot_key, headers=headers, data=data)

def main():
    # get_tieba('网络游戏', wx_robot_private, feishu_robot_private)
    get_tieba('逆水寒ol', wx_robot_private, feishu_robot_private)
    get_tieba('天涯明月刀ol', wx_robot_private, feishu_robot_private)
    get_tieba('魔兽玩家', wx_robot_private, feishu_robot_private)
    get_tieba('FF14', wx_robot_private, feishu_robot_private)
    get_tieba('剑网3', wx_robot_private, feishu_robot_private)
    get_tieba('白荆回廊', wx_robot_private, feishu_robot_private)
    get_tieba('古剑奇谭网络版', wx_robot_private, feishu_robot_private)
    # get_tieba('古剑奇谭网络版', robot_external)
    lock_file = 'tieba_spider.lock'
    if os.path.exists(lock_file):
        os.remove(lock_file)

if __name__ == "__main__":
    main()