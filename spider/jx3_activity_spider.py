from requests_html import HTMLSession
session = HTMLSession()

def main():
    li_all = []
    index_html = session.get("https://jx3.xoyo.com/hd/index.html")
    last_page = index_html.html.find('div.pagination > a:nth-child(9)', first=True)
    print(last_page.text, int(last_page.text))
    for n in range(1, int(last_page.text) + 1):
        article_list = getHtml(n)
        getCon(article_list, li_all)
        print(f"----第{n}页读取完毕----\n")
    # def sort_fun(elem):
    #     return elem["id"]
    # li_all.sort(key=sort_fun, reverse=True)
    print(f'共获取{len(li_all)}条')
    write_tab(li_all)


def getHtml(n=1):  # 获取单页JSON数据
    re = session.get(f"https://jx3.xoyo.com/hd/index.html?page={n}")
    # article_list = re.html.find('body > div.layout-wrapper > div > div > div.main_page > div > div.right > div.allnews_list_container > div > div > ul')
    article_list = re.html.find('ul.hd_list', first=True)
    print(article_list)
    return article_list

def getCon(article_list, li_all):
    li_list = article_list.find('article')
    for li in li_list:
        a = li.find('h3.hd_web_c_h3 > a', first=True)
        p = li.find('p.hd_web_c_text', first=True)
        date = li.find('p.hd_web_c_time', first=True)
        img = li.find('div.hd_web_c_l > a > img', first=True)
        # print(img.attrs['src'])
        # print(a.attrs['title'])
        # print(a.attrs['href'])
        # print(p.text)
        li_all.append({"title":a.attrs['title'], "href":a.attrs['href'], "text":p.text, "date":date.text, "img":img.attrs['src']})

def write_tab(li_all):
    text = "title\ttext\tdate\thref\timg\n"
    for li in li_all:
        text += (li["title"] + "\t" + li["text"] + "\t" + li["date"] + "\t" + li["href"] + "\t" + li["img"] + "\n")
    fileName = "jx3_activity.tab"
    with open(fileName, "w", encoding='gbk') as f:
        f.write(text)
        f.close()

if __name__ == "__main__":
    main()