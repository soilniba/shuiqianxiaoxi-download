from requests_html import HTMLSession
session = HTMLSession()

getPageNum = 200

def main():
    li_all = []
    for n in range(1, getPageNum + 1):
        article_list = getHtml(n)
        getCon(article_list, li_all)
        print("----第{}页读取完毕----\n".format(n))
    def sort_fun(elem):
        return elem["id"]
    li_all.sort(key=sort_fun, reverse=True)
    print('共获取{}条'.format(len(li_all)))
    write_tab(li_all)


def getHtml(n=1):  # 获取单页JSON数据
    re = session.get(f"https://jx3.xoyo.com/announce/index.html?page={n}")
    # article_list = re.html.find('body > div.layout-wrapper > div > div > div.main_page > div > div.right > div.allnews_list_container > div > div > ul')
    article_list = re.html.find('div.article_list > ul', first=True)
    # print(article_list)
    return article_list

def getCon(article_list, li_all):
    li_list = article_list.find('li')
    for li in li_list:
        a = li.find('a', first=True)
        em = li.find('em', first=True)
        # print(a.attrs['title'])
        # print(a.attrs['href'])
        # # /announce/gg.html?id=1329534
        # print(a.attrs['href'].split('?id=')[1])
        # print(em.text)
        li_all.append({"title":a.attrs['title'], "href":a.attrs['href'], "id":a.attrs['href'].split('?id=')[1], "date":em.text})

def write_tab(li_all):
    text = "id\ttitle\tdate\thref\n"
    for li in li_all:
        text += (li["id"] + "\t" + li["title"] + "\t" + li["date"] + "\t" + li["href"] + "\n")
    fileName = "jx3_announcement.tab"
    with open(fileName, "w", encoding='gbk') as f:
        f.write(text)
        f.close()

if __name__ == "__main__":
    main()