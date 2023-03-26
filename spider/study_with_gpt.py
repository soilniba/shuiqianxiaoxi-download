from bs4 import BeautifulSoup
import urllib
import json
import random
import time
import datetime
import requests
import os
import re
import csv
import gzip
import openai
from io import BytesIO
from PIL import Image
from requests_toolbelt import MultipartEncoder
from config import openai_api_key, feishu_robot_study, feishu_robot_error, wx_robot_error, wx_robot_study, feishu_app_id, feishu_app_secret, azure_api_key
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

def SearchBingImage(query, number):
    headers = {"Ocp-Apim-Subscription-Key": azure_api_key}
    url = f"https://api.bing.microsoft.com/v7.0/images/search?q={query}&count={number}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if "value" in data:
        image_urls = [item["contentUrl"] for item in data["value"]]
        image_key_list = []
        for url in image_urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.convert("RGB")  # 转换为RGB模式
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            image_bytes = buffered.getvalue()
            image_key = UpdateFeishuImage(image_bytes)
            if image_key:
                image_key_list.append(image_key)
        return image_key_list, image_urls

def GetFeishuToken():
    data = json.dumps({
        "app_id": feishu_app_id,
        "app_secret": feishu_app_secret,
    })
    response = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', headers=headers, data=data)
    responsejson = json.loads(response.text)
    print(responsejson['tenant_access_token'])
    return responsejson['tenant_access_token']

def UpdateFeishuImage(file):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (file)} 
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer ' + GetFeishuToken(),  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response
    responsejson = json.loads(response.text)
    if responsejson['code'] == 0:
        return responsejson['data']['image_key']
    else:
        send_error_msg('上传图片失败', response.text)

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

def send_message(text, image_key_list):
    title = '🌻小葵花妈妈课堂开课啦：'
    text = re.sub('\n+', '\n', text or '')
    feishu_msg = {"content": []}
    # feishu_msg["title"] = title
    feishu_msg["content"].append([
        {
            "tag": "text",
            "text": text
        },
    ])
    if image_key_list:
        images = []
        for image_key in image_key_list:
            images.append({
                    "tag": "img",
                    "image_key": image_key,
                })
        feishu_msg["content"].append(images)
    send_feishu_robot(feishu_robot_study, feishu_msg)
    # wx_msg = f'{title}\n{text}'
    # wx_msg = f'{text}'
    # send_wx_robot(wx_robot_study, wx_msg)

def random_project():
    with open("study_category_expand.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    total_subcategories = len(categories)
    subcategories_index_max = 0
    for subcategories_key in categories.keys():
        subcategories = categories[subcategories_key]['data']
        # categories[subcategories_key]['index'] = 0
        subcategories_index = categories[subcategories_key]['index']
        if subcategories_index > subcategories_index_max:
            subcategories_index_max = subcategories_index

    projects = []
    # 从可用项目中随机选出一个未被忽略的项目
    for _ in range(total_subcategories * 2):
        subcategories_key = random.choice(list(categories.keys()))
        subcategories_index = categories[subcategories_key]['index']
        if subcategories_index <= 0 or abs(subcategories_index_max - subcategories_index) >= total_subcategories * 0.6:
            # 为子类别分配一个index
            categories[subcategories_key]['index'] = subcategories_index_max + 1
            subcategories = categories[subcategories_key]['data']
            project_index_max = 0
            total_projects = 0
            for sub2categories_key in subcategories:
                sub2categories = subcategories[sub2categories_key]
                total_projects += len(sub2categories)
                for project_key in sub2categories:
                    # sub2categories[project_key] = 0
                    project_index = sub2categories[project_key]
                    if project_index > project_index_max:
                        project_index_max = project_index
            for _ in range(total_projects * 2):
                sub2categories_key = random.choice(list(subcategories.keys()))
                sub2categories = subcategories[sub2categories_key]
                project_key = random.choice(list(sub2categories.keys()))
                project_index = sub2categories[project_key]
                if project_index <= 0 or abs(project_index_max - project_index) >= total_projects * 0.6:
                    # 为项目分配一个index
                    sub2categories[project_key] = project_index_max + 1
                    projects.append({
                        'subcategorie': subcategories_key,
                        'sub2categorie': sub2categories_key,
                        'project': project_key,
                    })
                    break
        if projects:
            break

    # 将更新后的category.json写回文件
    with open("study_category_expand.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)

    return projects



def ask_gpt(project):
    # 设置要发送到API的提示语
    message = [
        {'role': 'system', 'content': f'你现在是{project["subcategorie"]}领域的专家,你的服务对象为30来岁有三五年工作经验的游戏策划,请在考虑他知识阅历经验的基础上提供服务,请避免太过浅显和太过常见的知识,最好是对他日后工作生活有所帮助的知识'},
        {'role': 'user', 'content': f'我希望了解一个{project["sub2categorie"]}中{project["project"]}方面的知识点,请你为我提供一段5分钟左右的学习内容,以这个知识点的中英文名称作为开头,介绍这个知识点并进行一些举例,讲解他的应用场景和优缺点,并为我提供一条扩展学习的文章(不需要链接)'},
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

def save_to_csv(project):
    filename = 'study_answer_save.csv'

    # 如果文件不存在，则创建一个新的空文件
    if not os.path.exists(filename):
        with open(filename, 'w+', newline='', encoding='utf-8') as f:
            pass

    # 打开CSV文件，使用追加模式
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['time', 'subcategorie', 'sub2categorie', 'project', 'answer', 'images'])
        # 如果文件是空的，则先写入表头
        if os.path.getsize(filename) == 0:
            writer.writeheader()
        writer.writerow(project)  # 追加数据

if __name__ == '__main__':
    for _ in range(2):
        for project in random_project():
            print(project)
            for i in range(10):
                answer = ask_gpt(project)
                if answer:
                    answer_key = answer.split('\n')[0]
                    image_key_list, image_urls = SearchBingImage(answer_key, 2)
                    send_message(answer, image_key_list)
                    project['answer'] = answer
                    project['images'] = image_urls
                    project['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    save_to_csv(project)
                    break