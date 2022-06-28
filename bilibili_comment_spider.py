import requests
import urllib3
import time
import re
import json

urllib3.disable_warnings()

Cookie = "rpdid=|(J|Juul|Yu~0J'ulYmukY~uu; LIVE_BUVID=22e6617dcad88821d026bd4afa037c8d; LIVE_BUVID__ckMd5=76a0a06d252f6de8; uTZ=-480; buvid3=79B529F5-2958-4EA2-BC4C-F5FEB9C665A8190953infoc; pgv_pvi=9384706048; balh_server_inner=__custom__; balh_is_closed=; fingerprint3=6d6627b980ebc93623882df60f535f21; fingerprint_s=51e98625e1da0339ed55aeec189e24cc; blackside_state=0; PVID=3; dy_spec_agreed=1; fingerprint=6994b151bf3ab31ec604d55edd5f6e59; buvid_fp_plain=AF7FB731-F36F-4AA4-A5B3-D91D3CB8CE3B143106infoc; SESSDATA=d7c8d57f,1650560447,031ec*a1; bili_jct=088cfb4eed7bf51741a1f17302ed34d3; DedeUserID=450370; DedeUserID__ckMd5=43bae8dba1c750d7; sid=6rk4l66i; _uuid=B28912B8-A85C-18F5-4DE0-ED8485E40E0C04287infoc; video_page_version=v_old_home; i-wanna-go-back=-1; b_ut=5; bp_video_offset_450370=621103999589829580; CURRENT_BLACKGAP=1; CURRENT_FNVAL=4048; buvid_fp=c7c103021f07b6f272eb49e7c9137b38; buvid4=6AD2FA36-16D5-E968-EF72-2BD163086C3A79756-022021002-iZljMiYNYufBsK0/aCPmmA==; CURRENT_QUALITY=112; SL_G_WPT_TO=zh-CN; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; bp_t_offset_450370=630077530682949653"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {
    'User-Agent': user_agent, 
    'Connection': 'keep-alive',
    'Cookie': Cookie,
}


def get_oid(BV_CODE: str) -> str:
    bv = BV_CODE[2:] if "BV" == BV_CODE[:2] else BV_CODE
    baseUrl = "http://api.bilibili.com/x/web-interface/view?bvid=" + bv
    ret = requests.get(baseUrl, headers=headers)
    data = json.loads(ret.content)['data']
    return data['aid'], data['title']
    # video_url = f"https://www.bilibili.com/video/BV{bv}"
    # r = requests.get(video_url, headers=headers, verify=False)
    # r.raise_for_status()
    # return re.search(r'content="https://www.bilibili.com/video/av(\d+)/">', r.text).group(1)


def get_data(page: int, oid: str):
    time.sleep(sleep_time)  # 减少访问频率，防止IP封禁
    api_url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&sort=2&_={int(time.time())}"
    print(f'正在处理:{api_url}')  # 由于需要减缓访问频率，防止IP封禁，打印访问网址以查看访问进程
    r = requests.get(api_url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()['data']['replies'], r.json()['data']['page']['count']


def get_folded_reply(page: int, oid: str, root: int):
    time.sleep(sleep_time)  # 减少访问频率，防止IP封禁
    url = f'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&ps=10&root={root}&_={int(time.time())}'
    print(f'正在处理:{url}')  # 由于需要减缓访问频率，防止IP封禁，打印访问网址以查看访问进程
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()['data']


def re_reply2(temp, root):
    _ = []
    for item in temp:
        if item[2] == root:
            _.append((item[1], 'FIRST'))
            continue
        for item2 in temp:
            if item[2] == item2[1]:
                _.append((item[1], item2[1]))
                break
        else:  # 回复对象被删除
            _.append((item[1], None))
    return _


def loop_folded_reply(root: int, rcount: int):
    temp = []
    temp2 = {}
    end_page = (rcount - 1) // 10 + 1 if (rcount-1) // 10 + 1 <= pages2 else pages2
    for page in range(1, end_page + 1):
        data = get_folded_reply(page, oid=oid, root=root)
        if not data['replies']:
            continue
        for item in data['replies']:
            mid = item['mid']
            rpid = item['rpid']
            parent = item['parent']
            dialog = item['dialog']
            rcount = item['rcount']
            like = item['like']
            ctime = item['ctime']
            name = item['member']['uname']
            # message = item['content']['message']
            message = re.sub(r'\t|\n|回复 @.*? :', '', item['content']['message'])
            # print(dialog, rpid, parent, name, message)
            temp.append([dialog, rpid, parent, name, message])
            temp2[rpid] = [mid, message, name, like, ctime]
        # else:
        #     break
    pointer = re_reply2(temp, root)

    def loop(pid, tab):
        # 用于递归查找单指
        for item in pointer:
            if pid == item[1]:
                mid, message, name, like, ctime = temp2[item[0]]
                f.write(
                    '|\t' * tab + f'|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
                loop(item[0], tab + 1)

    for rpid in [i for i, j in pointer if j == 'FIRST']:
        mid, message, name, like, ctime = temp2[rpid]
        f.write(
            f'|\t|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
        loop(rpid, tab=1)

    for ii, rpid in enumerate([i for i, j in pointer if not j]):
        if ii == 0:
            f.write(f'|\t|->\t评论已被删除\n')
        mid, message, name, like, ctime = temp2[rpid]
        f.write(
            f'|\t|\t|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
        loop(rpid, tab=3)


def get_reply(data, tab=0):
    if not data:
        return
    for item in data:
        mid = item['mid']
        rpid = item['rpid']
        count = item['count']
        rcount = item['rcount']
        like = item['like']
        ctime = item['ctime']
        name = item['member']['uname']
        message = re.sub(r'\t|\n|回复 @.*? :', '', item['content']['message'])
        f.write(
            '|\t' * tab + f'|->\t点赞：{like}\t评论："{message}"\tUSER：{name}(UID：{mid})\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}\n')
        print(f'处理评论:UID-{mid}\tUSER-{name}\t点赞-{like}')
        if 0 < rcount <= 3:
            get_reply(item['replies'], tab=1)
        elif rcount > 3:
            loop_folded_reply(root=rpid, rcount=rcount)


if __name__ == '__main__':
    pages1 = 10 # int(input('请输入爬取"视频评论"的页数(每页20条),推荐10:'))
    pages2 =  3 # int(input('请输入爬取"评论回复"的页数(每页10条),推荐03:'))
    sleep_time = 2.1  # 访问网页间隔，防止IP被禁，若运行程序后出现无法访问网页版BILIBILI评论区的现象，等待2小时即可~_~!
    BV_CODE = input('请输入视频BV号（比如BV19h411B7CD）:')# "BV19h411B7CD"  # 视频的BV号
    oid, title = get_oid(BV_CODE)

    f = open(f'{title}.txt', 'w', encoding='utf-8')
    # f = open(f'{title}-{time.strftime("%Y%m%d-%H%M")}.txt', 'w', encoding='utf-8')
    page = 1
    while True:
        try:
            data, reply_num = get_data(page, oid)
            get_reply(data)  # 遍历所有回复
            end_page = reply_num // 20 + 1 if reply_num // 20 + 1 <= pages1 else pages1
            if page == end_page:
                break
            page += 1
        except Exception as e:
            print('ERROR:', e)
            print('退出循环 结束')
            break
    f.close()