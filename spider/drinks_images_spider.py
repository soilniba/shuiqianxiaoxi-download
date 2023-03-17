from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
import urllib
import json
import time
import datetime
import requests
import os
import re
Cookie = 'cf_chl_2=a961dba7d44603f; cf_chl_prog=x11; cf_clearance=unHgoxtoewaBbyMCCC2IP3XIKpm2uIc1knYAj1IB0PI-1644832579-0-150; cppro-ft=true; cppro-ft-style=true; cppro-ft-style-temp=true; cp_style_61024=true'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27'
headers = {
    'User-Agent': user_agent, 
    'Connection': 'keep-alive',
    'Cookie': Cookie,
}

def getAll():
    for n in range(1, 12 + 1):
        if thread_list := getList(n):
            getPage(thread_list, n)
            print(f"----第{n}页读取完毕----")

def get_pic_file(url, file_patch):
    file_patch = f'drinks_images_big/{file_patch}'
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
                # print('下载图片成功', file_patch)
        except Exception as e:
                print('下载图片失败', file_patch)

def get_html(url):
        url = urllib.parse.quote(url, safe='/:?=&')
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print('python 返回 URL:{} 数据成功'.format(url))
        return html

def getList(n=1):  # 获取单页JSON数据
    url = f"https://www.thecookierookie.com/category/beverages/page/{n}/"
    HtmlContent = get_html(url)
    soup = BeautifulSoup(HtmlContent, "lxml")
    thread_list = soup.select_one('.content-sidebar-wrap')
    # print(thread_list)
    return thread_list

def getPage(thread_list, page_num):
    li_list = thread_list.select('img.aligncenter.post-image.entry-image')
    for li_num, li in enumerate(li_list, start=1):
        src = li.attrs['src']
        src = urllib.parse.quote(src)
        src = src.replace('https%3A//', 'https://')
        src = src.replace('-650x845', '')
        alt = li.attrs['alt']
        alt = re.sub('thecookierookie.com', '', alt, flags=re.IGNORECASE)
        alt = alt.replace('|', '').replace('\\', '_').replace('/', '_').replace('  ', ' ').strip().replace(' ', '_')
        alt = f'{page_num}.{li_num}_{alt}.jpg'
        print(src)
        print(alt)
        get_pic_file(src, alt)


def main():
    getAll()


if __name__ == "__main__":
    main()
