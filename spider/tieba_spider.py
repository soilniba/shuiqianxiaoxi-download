from bs4 import BeautifulSoup
import urllib
import json
import time
import datetime
import requests
import os
import re
import gzip
wx_robot_open = 'e012d034-7c19-4ee9-a713-9e674ec9ce34'
wx_robot_private = '36f924a9-4911-4c7f-aa36-900c01c44237'
wx_robot_error = 'a4973542-3002-4cab-b853-be6b815d4cfa'
feishu_robot_private = 'af4ca118-394a-4b55-96b8-3c7beb2d18c7'
feishu_robot_error = '34006ae3-b50a-48a6-9871-eb2a1b43223c'
Cookie = 'wise_device=0; USER_JUMP=-1; BDUSS=g1cmVEOGhtfk4xSG9uVVJvSzdSbjJLem9yd2pwcHB3ZVZRRDdwZUx5OXRuY2RpRVFBQUFBJCQAAAAAAAAAAAEAAADjrPwsx--z5sTWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG0QoGJtEKBiZF; BDUSS_BFESS=g1cmVEOGhtfk4xSG9uVVJvSzdSbjJLem9yd2pwcHB3ZVZRRDdwZUx5OXRuY2RpRVFBQUFBJCQAAAAAAAAAAAEAAADjrPwsx--z5sTWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG0QoGJtEKBiZF; 754756835_FRSVideoUploadTip=1; video_bubble754756835=1; BAIDUID=C9D7A2EF8537E9903056C364F5ED6533:FG=1; BIDUPSID=C9D7A2EF8537E9903056C364F5ED6533; PSTM=1666160893; delPer=0; PSINO=3; BAIDUID_BFESS=C9D7A2EF8537E9903056C364F5ED6533:FG=1; BAIDU_WISE_UID=wapp_1670227366212_397; bottleBubble=1; H_WISE_SIDS=110085_188746_202013_203519_204903_211986_213030_213345_214803_215730_216849_219623_219943_219946_222221_222624_223064_223323_224267_226627_227870_227932_228650_229154_229967_230583_230930_231500_231979_232054_234044_234050_234208_234295_234310_234316_234426_234722_234784_234928_235174_235200_235443_235512_235714_235980_236239_236242_236295_236312_236515_236537_236615_236940_237113_237240_237248_237649_237837_237965_238147_238429_238507_238511_238630_238755_238890_238958_238988_239006_239061_239102_239144_239281_239498_239605_239704_239834_239897_239947_240017_240046_240306_240334_240368_240447_240466_240598_240649_240744_240782_240890_241177_241207_241248_241297; rsv_i=2a16rJ5hpDkfmPdAGJIkeJgmo5H+N//+QZlaDriqBUG/63aFhpK9zEC4NiXLncC3LC13/yikWDuk68Jz3X5U7BeOHByXnt0; H_WISE_SIDS_BFESS=110085_188746_202013_203519_204903_211986_213030_213345_214803_215730_216849_219623_219943_219946_222221_222624_223064_223323_224267_226627_227870_227932_228650_229154_229967_230583_230930_231500_231979_232054_234044_234050_234208_234295_234310_234316_234426_234722_234784_234928_235174_235200_235443_235512_235714_235980_236239_236242_236295_236312_236515_236537_236615_236940_237113_237240_237248_237649_237837_237965_238147_238429_238507_238511_238630_238755_238890_238958_238988_239006_239061_239102_239144_239281_239498_239605_239704_239834_239897_239947_240017_240046_240306_240334_240368_240447_240466_240598_240649_240744_240782_240890_241177_241207_241248_241297; ZFY=V9:BLqCxEsCKi0O3ABeqk56U:BuOXCpk191ogL5zpTr2U:C; ZD_ENTRY=google; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1675158895; MCITY=-289:; STOKEN=760298bad8b96c90fc08f206e5c1df8e94ddec30c2b5b58a1a191679d1ff160c; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1677118755; BDRCVFR[l2BKebnsaG0]=mk3SLVN4HKm; H_PS_PSSID=26350; tb_as_data=f235e87810a241ac9554e5f7ead31fab888fbd1dac89c56e1cd883a0c05ab4ca254cd9e455385897932471849125eadbcee8d0b1d1f48d967d86dad62476c940c3d2b1eca7b23aa61e5ae7e03bdf836b36e6c7ad87708aa2900615f0c6a28b18; arialoadData=false; XFI=2b5d8ba0-be52-11ed-8c76-95d5bbc709f2; XFCS=102441FC385A8159AC75EFFBA14BA12C0B310B86C9ECF277FEF4B17F76DB4F19; XFT=2oKzrXj6Yw1I42t9huN8zRwkKHqGFWBmQ/ps6Aa6ANc=; RT="z=1&dm=baidu.com&si=daf702e1-fa6c-48e8-9120-b5f661cb8fe6&ss=lf0tzv34&sl=0&tt=0&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=2j8&ul=j7o"'
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
def get_tieba(tieba_name):
    global update_num, add_num
    update_num = 0
    add_num = 0
    file_name = f'tieba_{tieba_name}.json'
    json_all = load_json(file_name)
    clear_history_data(json_all)
    for n in range(0, 100, 50):
        if thread_list := getList(tieba_name, n):
            getPage(thread_list, json_all)
            print(f"----第{n + 50}条读取完毕----")
        else:
            print("thread_list读取失败")
            error_file_name = 'last_send_time_error.log'
            last_send_time = read_last_time(error_file_name)
            if time.time() - last_send_time > 29 * 60:  #报错间隔时间
                # markdown_msg = '# <font color="warning">出错啦！抓不到帖子啦！小彦宏出警啦！</font>'
                text_msg = '出错啦！抓不到帖子啦！小彦宏出警啦！'
                mentioned_list = [ 'wangchang@wangyuan.com' ]
                send_wx_robot(wx_robot_error, text_msg, mentioned_list)
                feishu_msg = {"content": []}
                feishu_msg["content"].append([
                    {
                        "tag": "text",
                        "text": '出错啦！抓不到帖子啦！小彦宏出警啦！'
                    },
                    # {
                    #     "tag": "at",
                    #     "user_id": "a5d2f73b",
                    # },
                ])
                at_list = GetUserIDs({
                    'wangchang@wangyuan.com',
                })
                # for user_id in at_list:
                    # feishu_msg["content"][0].append({
                    #     "tag": "at",
                    #     "user_id": user_id,
                    # })
                send_feishu_robot(feishu_robot_private, feishu_msg)
                write_last_time(error_file_name)
    # def sort_fun(elem):
    #     return elem["id"]
    # json_all.sort(key=sort_fun, reverse=True)
    print(f'{tieba_name}吧新增{add_num}条，更新{update_num}条')
    write_json(file_name, json_all)
    # time.sleep(5)
    # update_info(tieba_name, json_all)

def get_pic_file(url, file_patch):
    file_patch = f'images/{file_patch}'
    if not os.path.exists(file_patch):
        dir_path = os.path.split(file_patch)[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print('makedirs', file_patch, dir_path)
        # url = urllib.parse.quote(url, safe='/:?=&')
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        try:
            with open(file_patch, "wb") as code:
                code.write(response.read())
                print('下载图片成功', file_patch)
        except Exception as e:
                print('下载图片失败', file_patch)


def get_pic_all(data_info):
    if 'img_path_list' in data_info:
        data_tid = data_info['data_tid']
        img_path_list = data_info['img_path_list']
        for bpic, file_patch in img_path_list.items():
            get_pic_file(bpic, file_patch)
            # print(file_patch)

def get_html(url):
        url = urllib.parse.quote(url, safe='/:?=&')
        # request = urllib.request.Request(url, headers = headers)
        # response = urllib.request.urlopen(request)
        if proxies:
            response = requests.get(url, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, headers=headers)
        HtmlContent = response.read() if hasattr(response, 'read') else response.text
        # HtmlContent = response.read().decode('utf-8')
        # print('python 返回 URL:{} 数据成功'.format(url))
        return HtmlContent

def getList(tieba_name, n=0):  # 获取单页JSON数据
    url = f"https://tieba.baidu.com/f?kw={tieba_name}&ie=utf-8&pn={n}"
    HtmlContent = get_html(url)
    HtmlContent = HtmlContent.replace("<!--", "")
    HtmlContent = HtmlContent.replace("-->", "")
    soup = BeautifulSoup(HtmlContent, "lxml")
    thread_list = soup.select_one('#thread_list')
    # print(thread_list)
    return thread_list

def getPage(thread_list, json_all):
    dd = time.strftime("%d", time.localtime())
    yy_mm = time.strftime("%Y_%m", time.localtime())
    yy_mm_dd = time.strftime("%Y_%m_%d", time.localtime())
    yy_mm_dd_hh = time.strftime("%Y_%m_%d_%H", time.localtime())
    li_list = thread_list.select('li.j_thread_list.clearfix.thread_item_box')
    for li in li_list:
        # print(li.attrs['data-tid'])
        repo_num_str = li.select_one('span.threadlist_rep_num.center_text')
        repo_num = int(repo_num_str.text)
        # print(repo_num.text)
        title = li.select_one('a.j_th_tit')
        # print(title.attrs['href'], title.text)
        author = li.select_one('a.frs-author-name.j_user_card')
        # print(author.text, author.attrs['href'])
        last_repo = li.select_one('span.tb_icon_author_rely.j_replyer > a.frs-author-name.j_user_card')
        thread = li.select_one('div.threadlist_abs.threadlist_abs_onlyline')
        # img_ul = li.select_one('ul.threadlist_media.j_threadlist_media.clearfix')
        # img_list = None
        # if img_ul:
        #     img_list = img_ul.select('img.threadlist_pic.j_m_pic')
        #     for img in img_list:
        #         print('小图', img.attrs['data-original'])
        #         print('大图', img.attrs['bpic'])
        # json_all.append({"data-tid":li.attrs['data-tid'],})
        # 保存基本信息
        data_tid = li.attrs['data-tid']
        if data_tid in json_all:
            data_info = json_all[data_tid]
            if 'data_tid' not in data_info:
                data_info['data_tid'] = data_tid
        else:
            data_info = {}
            data_info['data_tid'] = data_tid
            data_info['title'] = title.text
            data_info['title_href'] = title.attrs['href']
            data_info['repo_num'] = repo_num
            data_info['author'] = author.text
            data_info['thread'] = thread and thread.text
            json_all[data_tid] = data_info
            global add_num
            add_num += 1
        if img_ul := li.select_one('ul.threadlist_media.j_threadlist_media.clearfix'):
            if img_list := img_ul.select('img.threadlist_pic.j_m_pic'):
                if 'img_path_list' not in data_info:
                    data_info['img_path_list'] = {}
                img_path_list = data_info['img_path_list']
                # if not type(data_info['img_list']) == type([]):
                #     data_info['img_list'] = []
                for img in img_list:
                    bpic = img.attrs['bpic']
                    if bpic not in img_path_list:
                        file_patch = f'{yy_mm}/{dd}/{data_tid}_{len(img_path_list)}.jpg'
                        img_path_list[bpic] = file_patch
        # 计数回复量
        repo_num_old = data_info['repo_num']
        data_info['repo_num'] = repo_num
        if repo_num > repo_num_old:
            global update_num
            update_num += 1
            data_info['update_time'] = time.time()
            repo_add = repo_num - repo_num_old

            if yy_mm_dd_hh in data_info:
                data_info[yy_mm_dd_hh] += repo_add
            else:
                data_info[yy_mm_dd_hh] = repo_add

            if yy_mm_dd in data_info:
                data_info[yy_mm_dd] += repo_add
            else:
                data_info[yy_mm_dd] = repo_add

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

# def update_info(tieba_name, json_all):
#     yy_mm_dd = time.strftime("%Y_%m_%d", time.localtime()) 
#     yy_mm_dd_hh = time.strftime("%Y_%m_%d_%H", time.localtime()) 
#     update_list = []
#     for data_tid, data_info in  json_all.items():
#         if yy_mm_dd in data_info:
#             if data_info[yy_mm_dd] >= 1:
#                 update_list.append(data_info)
#     if len(update_list) > 0:
#         markdown_msg = '{}贴吧今日热贴：\n'.format(tieba_name)
#         # print(markdown_msg)
#         def sort_fun(data_info):
#             return data_info[yy_mm_dd]
#         update_list.sort(key=sort_fun, reverse=True)
#         # for data_info in update_list:
#         for i in range(0, min(10, len(update_list))):
#             data_info = update_list[i]
#             markdown_msg += '><font color=\"warning\">{}</font>条回复：[{}](https://tieba.baidu.com/{})\n'.format(data_info[yy_mm_dd], data_info['title'], data_info['title_href'])
#             # print('{}条：{}'.format(data_info[yy_mm_dd], data_info['title']))
#         print(markdown_msg)
#         file_name = 'last_send_time_{}.log'.format(tieba_name)
#         last_send_time = read_last_time(file_name)
#         if time.time() - last_send_time > 50 * 60:  #每小时发布一次
#             send_wx_robot(robot_open, markdown_msg)
#             write_last_time(file_name)
#             # with open('runtime.log', "a") as f:
#             #     f.write(time.strftime("%Y/%m/%d_%T\n", time.localtime()) )
#             #     f.close()

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

def clear_history_data(json_all):
    today = datetime.date.today()
    pattern = '(\d{4})_(\d{2})_(\d{2})'
    compile_1 = re.compile(pattern)
    for data_tid in list(json_all.keys()):
        data_info = json_all[data_tid]
        min_interval_day = 999
        for yyyy_mm_dd_hh, num in data_info.items():
            if match := compile_1.match(yyyy_mm_dd_hh):
                yyyy, mm, dd = match.groups()
                date_this = datetime.date(int(yyyy), int(mm), int(dd))
                interval = today - date_this
                if interval.days < min_interval_day:
                    min_interval_day = interval.days
                    # print(interval, interval.days)
                    # print(yyyy_mm_dd_hh, yyyy, mm, dd)
        if min_interval_day > 30 and min_interval_day != 999:
            print('del old item', data_tid, data_info['title'], min_interval_day)
            del json_all[data_tid]


def main():
    lock_file = 'tieba_spider.lock'
    if not os.path.exists(lock_file):
        _extracted_from_main_4(lock_file)
    else:
        print('file lock')
        time.sleep(5)
        os.remove(lock_file)
        print('lock file delete')


# TODO Rename this here and in `main`
def _extracted_from_main_4(lock_file):
    with open(lock_file, 'w') as f:
        f.write('')
        f.close()
    # 设置代理
    # opener = urllib.request.build_opener(proxy_handler)
    # urllib.request.install_opener(opener)
    get_tieba('古剑奇谭网络版')
    get_tieba('白荆回廊')
    # get_tieba('网络游戏')
    get_tieba('逆水寒ol')
    get_tieba('天涯明月刀ol')
    get_tieba('FF14')
    get_tieba('魔兽玩家')
    get_tieba('剑网3')
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


    # GetUserIDs({
    #     'wangchang@wangyuan.com',
    #     'zhanglei@wangyuan.com',
    #     'pansong@wangyuan.com',
    # })
    # feishu_msg = {"content": []}
    # feishu_msg["content"].append([
    #     {
    #         "tag": "text",
    #         "text": '出错啦！抓不到帖子啦！小彦宏出警啦！'
    #     },
    #     {
    #         "tag": "at",
    #         "user_id": "a5d2f73b",
    #     },
    # ])
    # send_feishu_robot(feishu_robot_error, feishu_msg)