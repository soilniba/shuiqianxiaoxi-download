from bs4 import BeautifulSoup
import random
import json
import time
import requests
from config import wx_robot_open, wx_robot_private, wx_robot_error, wx_robot_external, feishu_robot_private, feishu_robot_open, feishu_robot_error

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
    yy_mm_dd = time.strftime("%Y_%m_%d", time.localtime())
    update_list = []
    for data_tid, data_info in  json_all.items():
        if yy_mm_dd in data_info:
            if data_info[yy_mm_dd] > 1:
                update_list.append(data_info)
    if update_list:
        markdown_msg = '👉<font color=\"info\">{}吧</font>👈今日热贴：\n'.format(tieba_name)
        feishu_msg = {"content": []}
        feishu_msg["title"] = '👉{}吧👈今日热贴：'.format(tieba_name)
        # print(markdown_msg)
        def sort_fun(data_info):
            return data_info[yy_mm_dd]

        update_list.sort(key=sort_fun, reverse=True)
        random_emoji_list = random.sample(flag_emoji_list, len(flag_emoji_list))
        # for data_info in update_list:
        for i in range(min(10, len(update_list))):
            data_info = update_list[i]
            emoji = '🚩'
            if i == 0:
                emoji = '🔥🔥🔥'
            elif i == 1:
                emoji = '🔥🔥'
            elif i == 2:
                emoji = '🔥'
            else:
                emoji = random_emoji_list.pop()
                # emoji = random.choice(flag_emoji_list)
            markdown_msg += '><font color=\"warning\">{0}</font>条回复：{3}[{1}](https://tieba.baidu.com{2})\n'.format(data_info[yy_mm_dd], data_info['title'], data_info['title_href'], emoji)
            feishu_msg["content"].append([
                {
                    "tag": "text",
                    "text": '{}条回复：{}'.format(data_info[yy_mm_dd], emoji)
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
    get_tieba('古剑奇谭网络版', wx_robot_open, feishu_robot_open)
    # get_tieba('古剑奇谭网络版', robot_external)

if __name__ == "__main__":
    main()