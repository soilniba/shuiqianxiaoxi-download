#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File: getSub.py
@Description: 爬取《睡前消息》节目简介中的新闻事件
@Time: 2020/05/29 14:32:17
@Author: 盛亚琪
@Blog: i.2017.work
'''

import subprocess
import requests
import xlwt


def main():
    li = []
    for n in range(1, 2):
        print("保存第", n, "页")
        root = getJson(n)
        getCon(root, li)
    # priIt(li)        # 打印markdown格式文本
    # saveXl(li)     # 保存excel
    # priIt_Bili(li)  # 打印B站专栏富文本格式
    # sorted(li, key = itemgetter(4))
    def sort_fun(elem):
        return elem["created"]
    li.sort(key=sort_fun, reverse=True)
    # sorted(li, key=aid)
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
            # li.append([v["title"], v["description"], v["play"], v["aid"], v["bvid"]])


def saveXl(li):
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("sheet1")
    col = ["标题", "简介", "播放量", "aid"]
    for i in range(len(col)):
        ws.write(0, i, col[i])
    for i in range(1, len(li)+1):
        ws.write(i, 0, li[i-1][0])
        ws.write(i, 1, li[i-1][1])
        ws.write(i, 2, li[i-1][2])
        ws.write(i, 3, li[i-1][3])
    wb.save("《睡前消息》节目往期新闻事件索引.xls")


def priIt(li):
    pr = ""
    for i in li:
        pr += ("\n"+"### "+str(i[0])+"\n" + "------"+"\n" +
               "播放量: "+str(i[2])+"     ["+"AV"+str(i[3])+"]"+"("+"https://www.bilibili.com/video/av"+str(i[3])+")" + "\n\n" + str(i[1]))
    with open("README.md", "w", encoding='utf-8') as f:
        f.write(pr)
        f.close()


def priIt_Bili(li):
    pr = ""
    for i in li:
        pr += ("\n\n"+"**"+str(i[0])+"**"+"\n" + "\n" +
               "播放量: " + str(i[2]) + "     av" + str(i[3]) + "\n\n" + str(i[1]))
    with open("《睡前消息》节目往期新闻事件索引.md", "w", encoding='utf-8') as f:
        f.write(pr)
        f.close()


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
