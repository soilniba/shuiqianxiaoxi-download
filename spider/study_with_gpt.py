from bs4 import BeautifulSoup
import urllib
import json
import random
import time
import datetime
import requests
import os
import re
import gzip
import openai
from config import openai_api_key, feishu_robot_study, feishu_robot_error, wx_robot_error, wx_robot_study
openai.api_key = openai_api_key
import psutil
p = psutil.Process()                                        # 获取当前进程的Process对象
p.nice(psutil.IDLE_PRIORITY_CLASS)                          # 设置进程为低优先级
script_dir = os.path.dirname(os.path.realpath(__file__))    # 获取脚本所在目录的路径
os.chdir(script_dir)                                        # 切换工作目录到脚本所在目录

# feishu_robot_study = feishu_robot_error                     # 强制使用测试频道
# wx_robot_study = wx_robot_error                             # 强制使用测试频道

Cookie = ''
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {
    'User-Agent': user_agent, 
    'Connection': 'close',
    'Cookie': Cookie,
    'Accept-Encoding': 'gzip',
}

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
    response = requests.post(f'https://open.feishu.cn/open-apis/bot/v2/hook/{feishu_robot_key}', headers=headers, data=data)
    return json.loads(response.text)

def send_wx_robot(robot_url, markdown_msg):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "msgtype": "markdown", 
        "markdown": { "content": markdown_msg },
    })
    response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_url, headers=headers, data=data)

def send_error_msg(text):
    text_msg = text
    feishu_msg = {"content": []}
    feishu_msg["content"].append([
        {
            "tag": "text",
            "text": text_msg
        },
    ])
    send_feishu_robot(feishu_robot_error, feishu_msg)

def send_message(text):
    title = '🌻小葵花妈妈课堂开课啦：'
    text = re.sub('\n+', '\n', text or '')
    feishu_msg = {"content": []}
    feishu_msg["title"] = title
    feishu_msg["content"].append([
        {
            "tag": "text",
            "text": text
        },
    ])
    send_feishu_robot(feishu_robot_study, feishu_msg)
    wx_msg = f'{title}\n{text}'
    # send_wx_robot(wx_robot_study, wx_msg)

def random_project():
    with open("study_category.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    category_list = ["通识教育"]
    chosen_categories = random.sample(category_list, 1)

    projects = []

    # 从study_config.json中读取index的初始值
    if os.path.exists("study_config.json"):
        with open("study_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            index = config.get("project_index", 0)
    else:
        index = 0

    total_projects = 0
    for category_key in chosen_categories:
        category = categories[category_key]
        for subcategories_key in category.keys():
            subcategories = category[subcategories_key]
            total_projects += len(subcategories)

    # project_key
    # 从可用项目中随机选出一个未被忽略的项目
    for _ in range(total_projects * 2):
        # project_index, category
        for category_key in chosen_categories:
            category = categories[category_key]
            subcategories_key = random.choice(list(category.keys()))
            subcategories = category[subcategories_key]
            project_key = random.choice(list(subcategories.keys()))
            project_index = subcategories[project_key]
        if project_index <= 0 or abs(project_index - index) >= total_projects * 0.6:
            # 为项目分配一个index
            subcategories[project_key] = index
            projects.append({
                'index': index,
                'project': project_key,
                'subcategories': subcategories_key,
                'category': category_key
            })
            index += 1
            break


    # 将更新后的index值写回study_config.json
    with open("study_config.json", "w", encoding="utf-8") as f:
        json.dump({"project_index": index}, f)

    # 将更新后的category.json写回文件
    with open("study_category.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)

    return projects



def ask_gpt(project):
    # 设置要发送到API的提示语
    message = [
        {'role': 'system', 'content': f'你现在是{project["subcategories"]}领域的专家,你的服务对象为30来岁有三五年工作经验的游戏策划,请在考虑他知识阅历经验的基础上提供服务,请避免太过浅显和太过常见的知识,最好是对他日后工作生活有所帮助的知识'},
        {'role': 'user', 'content': f'我希望了解一个{project["project"]}方面的知识点,你为我提供一段5分钟左右的学习内容,介绍这个知识点并进行一些举例,讲解他的应用场景和优缺点,并为我提供一条扩展学习的文章(不需要链接)'},
    ]
    print(message)
    try:
        response = openai.ChatCompletion.create(
            # model = "gpt-3.5-turbo",  # 对话模型的名称
            model = "gpt-4",  # 对话模型的名称
            messages = message,
            #max_tokens=4096,  # 回复最大的字符数
            # temperature = 0.9,  # 值在[0,1]之间，越大表示回复越具有不确定性
            # top_p = 1,
            # frequency_penalty = 0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            # presence_penalty = 0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
        )
        print(
            f"""[ChatGPT] reply={response.choices[0]['message']['content']}, total_tokens={response["usage"]["total_tokens"]}"""
        )
        return response.choices[0]['message']['content']
    except Exception as e:
        print(e)
        send_error_msg(f'openai api error:{e}')

if __name__ == '__main__':
    for _ in range(2):
        for project in random_project():
            print(project)
            if answer := ask_gpt(project):
                send_message(answer)
