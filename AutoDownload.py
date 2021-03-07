import subprocess
import requests

getAllIndex = 0
getShuiIndex = 0
getOtherIndex = 0
downloadNum = 20
getPageNum = 2
onePageVideoNum = 100

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


def getJson(n=1):  # 获取单页JSON数据
    re = requests.get(
        "https://api.bilibili.com/x/space/arc/search?mid=316568752&ps={}&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp".format(onePageVideoNum, n))
    re.encoding = ("utf-8")
    root = re.json()
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
    pr = ""
    i = 0
    for v in li:
        i += 1
        if i > downloadNum:  #下载最近几条
            break
        pr += ("\nrem " + str(v["title"]))
        pr += ("\nyou-get -c netscape_cookie.txt https://www.bilibili.com/video/av" + str(v["aid"]))
        # pr += ("\nyou-get -c netscape_cookie.txt https://www.bilibili.com/video/" + str(v["bvid"]))
    fileName = "you-get_download.bat"
    with open(fileName, "w", encoding='gbk') as f:
        f.write(pr)
        f.close()
    subprocess.run(fileName)

if __name__ == "__main__":
    main()
