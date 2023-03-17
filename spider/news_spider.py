from bs4 import BeautifulSoup
import urllib
import json
import time
import datetime
import requests
import os
import re
import gzip

# 获取脚本所在目录的路径
script_dir = os.path.dirname(os.path.realpath(__file__))

# 切换工作目录到脚本所在目录
os.chdir(script_dir)

feishu_robot_news = '8d3aa15c-8ede-4e7b-a0ae-335fce9b3bb7'
feishu_robot_error = '34006ae3-b50a-48a6-9871-eb2a1b43223c'
Cookie = ''
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {
    'User-Agent': user_agent, 
    'Connection': 'close',
    'Cookie': Cookie,
    'Accept-Encoding': 'gzip',
}
# proxy_handler = urllib.request.ProxyHandler({'socks5': '127.0.0.1:1080'})
# proxy_handler = urllib.request.ProxyHandler({'socks5': 'k814.kdltps.com:20818'})
socks5_proxies = 'socks5://t17842936906948:8z10sobl@l854.kdltps.com:20818'
# socks5_proxies = 'socks5://127.0.0.1:1080'
proxies = {
    'http': socks5_proxies,
    'https': socks5_proxies,
}
proxies = None

update_num = 0
add_num = 0
def get_news():
    global update_num, add_num
    update_num = 0
    add_num = 0
    file_name = 'news_gov.json'
    json_all = load_json(file_name)
    # clear_history_data(json_all)
    new_news_list = []
    if thread_list := get_list():
        get_page(thread_list, json_all, new_news_list)
        print("----新闻读取完毕----")
    else:
        print("thread_list读取失败")
        error_file_name = 'last_send_time_error.log'
        last_send_time = read_last_time(error_file_name)
        if time.time() - last_send_time > 29 * 60:  #报错间隔时间
            text_msg = '出错啦！抓不到新闻啦！'
            feishu_msg = {"content": []}
            feishu_msg["content"].append([
                {
                    "tag": "text",
                    "text": text_msg
                },
            ])
            send_feishu_robot(feishu_robot_error, feishu_msg)
            write_last_time(error_file_name)
    print(f'新闻新增{add_num}条')
    write_json(file_name, json_all)
    if new_news_list:
        send_news(new_news_list)

def send_news(new_news_list):
    feishu_msg = {"content": []}
    # feishu_msg["title"] = '刚刚收到的新消息：'
    # for data_info in update_list:
    for data_info in new_news_list:
        feishu_msg["content"].append([
            {
                "tag": "text",
                "text": data_info['date']
            },
            {
                "tag": "a",
                "text": data_info['title'],
                "href": f'http://www.gov.cn{data_info["href"]}'
            }
        ])
    send_feishu_robot(feishu_robot_news, feishu_msg)

def get_html(url):
        url = urllib.parse.quote(url, safe='/:?=&')
        # request = urllib.request.Request(url, headers = headers)
        # response = urllib.request.urlopen(request)
        if proxies:
            response = requests.get(url, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        HtmlContent = response.read() if hasattr(response, 'read') else response.text
        # HtmlContent = HtmlContent.decode('utf-8')
        # print('python 返回 URL:{} 数据成功'.format(url))
        return HtmlContent

def get_list():  # 获取单页JSON数据
    url = "http://www.gov.cn/xinwen/lianbo/bumen.htm"
    HtmlContent = get_html(url)
    HtmlContent = HtmlContent.replace("<!--", "")
    HtmlContent = HtmlContent.replace("-->", "")
    soup = BeautifulSoup(HtmlContent, "lxml")
    thread_list = soup.select_one('body > div.main > div > div > div.news_box > div')
    # print(thread_list)
    return thread_list

def get_page(thread_list, json_all, new_news_list):
    li_list = thread_list.select('li')
    for li in li_list:
        a = li.select_one('a')
        title = a.text
        href = a.attrs['href']
        span = li.select_one('span')
        date = span.text.strip()
        # print(title, href, date)
        if href in json_all:
            data_info = json_all[href]
            if 'href' not in data_info:
                data_info['href'] = href
        else:
            data_info = {}
            data_info['href'] = href
            data_info['title'] = title
            data_info['date'] = date
            json_all[href] = data_info
            # new_news_list.append(data_info)
            new_news_list.insert(0, data_info)
            global add_num
            add_num += 1


def write_json(file_name, json_all):
    str_json = json.dumps(json_all, indent=2, ensure_ascii=False)
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(str_json)
        f.close()

def load_json(file_name):
    try:
        f = open(file_name, "r", encoding='utf-8')
    except IOError:
        return {}
    else:
        return json.load(f)

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
    response = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={robot_url}', headers=headers, data=data)

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

def get_feishu_token():
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "app_id": "cli_a1c3790e21f8100c",
        "app_secret": "YVXgZL2HnYi6gHm2NmxenfOTi60rfrQ3",
    })
    response = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', headers=headers, data=data)
    responsejson = json.loads(response.text)
    print(responsejson['tenant_access_token'])
    return responsejson['tenant_access_token']

def GetUserIDs(email_list):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + get_feishu_token(),
    }
    response = requests.post('https://open.feishu.cn/open-apis/user/v1/batch_get_id?emails=' + '&emails='.join(email_list), headers=headers)
    responsejson = json.loads(response.text)
    email_users = responsejson['data']['email_users']
    user_id_list = []
    for email, ids in email_users.items():
        print(email, ids[0]['open_id'], ids[0]['user_id'])
        user_id_list.append(ids[0]['user_id'])
    return user_id_list

def write_last_time(file_name):
    with open(file_name, "w") as f:
        f.write(str(time.time()))
        f.close()

def read_last_time(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            last_send_time = float(f.read())
            f.close()
            return last_send_time
    else:
        write_last_time(file_name)
        return time.time()

def main():
    lock_file = 'news_spider.lock'
    if not os.path.exists(lock_file):
        _extracted_from_main_4(lock_file)
    else:
        print('file lock')
        time.sleep(5)
        os.remove(lock_file)
        print('lock file delete')

def _extracted_from_main_4(lock_file):
    # with open(lock_file, 'w') as f:
    #     f.write('')
    #     f.close()
    get_news()
    if os.path.exists(lock_file):
        os.remove(lock_file)

def check_local_ip():
    url = 'https://www.123cha.com'
    HtmlContent = get_html(url)
    soup = BeautifulSoup(HtmlContent, "lxml")
    iplocation = soup.select_one('body > div.header > div.location > span')
    print('当前访问IP:', iplocation and iplocation.text)

if __name__ == "__main__":
    try:
        # 可能会引发异常的代码
        check_local_ip()
    except Exception as e:
        # 处理异常的代码
        print('Error:', e)
        result = None
    main()
