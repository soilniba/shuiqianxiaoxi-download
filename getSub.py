import subprocess
import requests

def main():
    li = []
    for n in range(1, 2):
        print("保存第", n, "页")
        root = getJson(n)
        getCon(root, li)
    def sort_fun(elem):
        return elem["created"]
    li.sort(key=sort_fun, reverse=True)
    priIt_Youget(li)  # you-get下载批处理文件


def getJson(n=1):  # 获取单页JSON数据
    re = requests.get(
        "https://api.bilibili.com/x/space/arc/search?mid=316568752&ps=100&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp".format(n))
    re.encoding = ("utf-8")
    root = re.json()
    return root


def getCon(root, li):  # 传入JSon解析内容进列表
    for v in root["data"]["list"]["vlist"]:
        if "【睡前消息" in v["title"]:
            li.append({"aid":v["aid"], "bvid":v["bvid"], "title":v['title'], "description":v["description"], "created":v["created"]})

def priIt_Youget(li):
    pr = ""
    i = 0
    for v in li:
        i += 1
        if i > 5:  #下载最近几条
            break
        pr += ("\nrem " + str(v["title"]))
        pr += ("\nrem you-get -c netscape_cookie.txt https://www.bilibili.com/video/av" + str(v["aid"]))
        # pr += ("\nyou-get -c netscape_cookie.txt https://www.bilibili.com/video/" + str(v["bvid"]))
    fileName = "you-get_download.bat"
    with open(fileName, "w", encoding='gbk') as f:
        f.write(pr)
        f.close()
    subprocess.run(fileName)

if __name__ == "__main__":
    main()
