import urllib
import json
import time
import datetime
import requests
import os
import re
import random
from requests_toolbelt import MultipartEncoder


feishu_robot_error = '34006ae3-b50a-48a6-9871-eb2a1b43223c'
feishu_robot_biaoqing_qihua = 'b9e4bd76-2d67-4628-a4eb-d7aaba01d019'
feishu_robot_biaoqing_fanquan = '974c4517-d936-4987-8b25-206fa4430bbb'
Cookie = ''
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {
    'User-Agent': user_agent, 
    'Connection': 'keep-alive',
    'Cookie': Cookie,
}
feishu_token = None

def GetFeishuToken():
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        # 表情包抽查
        "app_id": "cli_a23fe7a544b91013",
        "app_secret": "9TiQKnNse8lFkCgKbBYBN3y7fXKiOwTT",
    })
    response = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', headers=headers, data=data)
    responsejson = json.loads(response.text)
    print(responsejson['tenant_access_token'])
    return responsejson['tenant_access_token']

def GetFeishuChatsID():
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + feishu_token,
    }
    response = requests.get('https://open.feishu.cn/open-apis/im/v1/chats?user_id_type=open_id&page_size=50', headers=headers)
    responsejson = json.loads(response.text)
    # print(responsejson['data']['items'])
    if responsejson['msg'] == 'ok':
        for item in responsejson['data']['items']:
            print(item['name'], item['chat_id'])
            if '表情' in item['name']:
                return item['chat_id']
        print('未找到表情包群ID')
    else:
        print('数据获取异常', responsejson['msg'])

def SendFeishuRobot(feishu_robot_key, feishu_msg):
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


def GetFeishuImage(image_key, message_id):
    headers = {
        'Authorization': 'Bearer ' + feishu_token,
    }
    response = requests.get(f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{image_key}?type=image', headers=headers)
    return response.content

def GetFeishuName(user_id, id_type):
    headers = {
        'Authorization': 'Bearer ' + feishu_token,
    }
    response = requests.get(f'https://open.feishu.cn/open-apis/contact/v3/users/{user_id}?user_id_type={id_type}', headers=headers)
    responsejson = json.loads(response.text)
    return responsejson['data']['user']

def UpdateFeishuImage(file):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (file)}  # 需要替换具体的path 
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer ' + feishu_token,  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response
    responsejson = json.loads(response.text)
    return responsejson['data']['image_key']

def GetFeishuMessages(chats_id, page_token = ''):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + feishu_token,
    }
    url = 'https://open.feishu.cn/open-apis/im/v1/messages' + \
        f"?container_id={chats_id}&container_id_type=chat&page_size=50&start_time={0}&page_token={page_token}"
        # ?start_time={int(time.time() - 24*60*60)}
    # print(url)
    response = requests.get(url, headers=headers)
    responsejson = json.loads(response.text)
    if responsejson['msg'] == 'ok':
        return responsejson['data']['items'], responsejson['data']['has_more'], responsejson['data']['page_token']
    else:
        print('数据获取异常', responsejson['msg'])
    # print('未找到表情包群ID')
    return None, None

def GetMessagesAll(chats_id):
    has_more = True
    page_token = ''
    items_all = []
    for i in range(0, 100):
        if has_more:
            items, has_more, page_token = GetFeishuMessages(chats_id, page_token)
            if items:
                for item in items:
                    if item['msg_type'] == 'image':
                        items_all.append(item)
    if items_all and len(items_all) > 0:
        item = random.choice(items_all)
        print(item['message_id'], item['body']['content'], item['update_time'], item['sender']['id'], item['sender']['id_type'], item['msg_type'])
        feishu_msg = {"content": []}
        img_info = json.loads(item['body']['content'])
        file = GetFeishuImage(img_info['image_key'], item['message_id'])
        image_key = UpdateFeishuImage(file)
        sender_info = GetFeishuName(item["sender"]["id"], item["sender"]["id_type"])
        sender_name = f'[{sender_info["name"]}]'
        # if sender_info["description"] != '':
        #     sender_name += f'({sender_info["description"]})'
        feishu_msg["content"].append([
            {
                "tag": "img",
                "image_key": image_key,
            },
            {
                "tag": "text",
                "text": f'表情管理大师{sender_name}穿越过来分享了一下{time.strftime("%Y年%m月%d日%H点%M分", time.localtime(int(item["update_time"])/1000))}的心情',
            },
        ])

        SendFeishuRobot(feishu_robot_biaoqing_fanquan, feishu_msg)
        # for item in items_all:
        #     print(item['body']['content'], item['update_time'], item['sender']['id'], item['msg_type'])


def main():
    global feishu_token
    feishu_token = GetFeishuToken()
    GetMessagesAll(GetFeishuChatsID())

if __name__ == "__main__":
    main()