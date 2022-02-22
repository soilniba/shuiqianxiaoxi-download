import subprocess
import requests
import json
import os
import urllib

Cookie = "rpdid=|(J|Juul|Yu~0J'ulYmukY~uu; LIVE_BUVID=22e6617dcad88821d026bd4afa037c8d; LIVE_BUVID__ckMd5=76a0a06d252f6de8; uTZ=-480; buvid3=79B529F5-2958-4EA2-BC4C-F5FEB9C665A8190953infoc; pgv_pvi=9384706048; balh_server_inner=__custom__; balh_is_closed=; fingerprint3=6d6627b980ebc93623882df60f535f21; fingerprint_s=51e98625e1da0339ed55aeec189e24cc; blackside_state=0; PVID=3; dy_spec_agreed=1; fingerprint=6994b151bf3ab31ec604d55edd5f6e59; buvid_fp_plain=AF7FB731-F36F-4AA4-A5B3-D91D3CB8CE3B143106infoc; SESSDATA=d7c8d57f,1650560447,031ec*a1; bili_jct=088cfb4eed7bf51741a1f17302ed34d3; DedeUserID=450370; DedeUserID__ckMd5=43bae8dba1c750d7; sid=6rk4l66i; _uuid=B28912B8-A85C-18F5-4DE0-ED8485E40E0C04287infoc; video_page_version=v_old_home; i-wanna-go-back=-1; b_ut=5; bp_video_offset_450370=621103999589829580; CURRENT_BLACKGAP=1; CURRENT_FNVAL=4048; buvid_fp=c7c103021f07b6f272eb49e7c9137b38; buvid4=6AD2FA36-16D5-E968-EF72-2BD163086C3A79756-022021002-iZljMiYNYufBsK0/aCPmmA==; CURRENT_QUALITY=112; SL_G_WPT_TO=zh-CN; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; bp_t_offset_450370=630077530682949653"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {
    'User-Agent': user_agent, 
    'Connection': 'keep-alive',
    'Cookie': Cookie,
}

getAllIndex = 0
getShuiIndex = 0
getOtherIndex = 0
downloadNum = 20
getPageNum = 2
onePageVideoNum = 50

def main():
    li = []
    for n in range(1, getPageNum + 1):
        root = getJson(n)
        getCon(root, li)
        print("----第{}页读取完毕----\n".format(n))
    def sort_fun(elem):
        return elem["created"]
    print("\n共读取{}页×{}共{}条视频，其中：".format(getPageNum, onePageVideoNum, getAllIndex))
    print("\t睡前消息{}条".format(getShuiIndex))
    print("\t其他视频{}条".format(getOtherIndex))
    print("开始下载前{}条睡前消息和弹幕".format(downloadNum))
    li.sort(key=sort_fun, reverse=True)
    priIt_Youget(li)  # you-get下载批处理文件


def get_html(url):
        url = urllib.parse.quote(url, safe='/:?=&')
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print('python 返回 URL:{} 数据成功'.format(url))
        return html

def getJson(n=1):  # 获取单页JSON数据
    url = "https://api.bilibili.com/x/space/arc/search?mid=316568752&ps={}&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp".format(onePageVideoNum, n)
        #   "https://api.bilibili.com/x/space/arc/search?mid=316568752&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
    # re = requests.get(url)
    # re.encoding = ("utf-8")
    # root = re.json()
    re = get_html(url)
    root = json.loads(re)
    return root

def getCon(root, li):  # 传入JSon解析内容进列表
    global getAllIndex, getShuiIndex, getOtherIndex
    for v in root["data"]["list"]["vlist"]:
        getAllIndex += 1
        if "【睡前消息" in v["title"]:
            getShuiIndex += 1
            print(v["title"])
            li.append({"aid":v["aid"], "bvid":v["bvid"], "title":v['title'], "description":v["description"], "created":v["created"]})
        else:
            getOtherIndex += 1
            print("※", v["title"])

def priIt_Youget(li):
    pr = "cd /d %~dp0"
    i = 0
    for v in li:
        i += 1
        if i > downloadNum:  #下载最近几条
            break
        pr += ("\nrem " + str(v["title"]))
        pr += ("\nyou-get -c netscape_cookie.txt https://www.bilibili.com/video/av" + str(v["aid"]))
        # pr += ("\nyou-get -c netscape_cookie.txt https://www.bilibili.com/video/" + str(v["bvid"]))
    filePath = os.path.split(os.path.realpath(__file__))[0]
    fileName = filePath + "\you-get_download.bat"
    with open(fileName, "w", encoding='gbk') as f:
        f.write(pr)
        f.close()
    subprocess.run(fileName)

if __name__ == "__main__":
    main()
