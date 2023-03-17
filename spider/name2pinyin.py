
import csv
from pypinyin import pinyin, lazy_pinyin, Style

def main():
    with open("name2pinyin333.csv", "w", encoding='UTF-8') as csvFile333:
        spamwriter = csv.writer(csvFile333, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        with open('name2pinyin222.csv', newline='', encoding='UTF-8') as csvFile222:
            csv_reader = csv.reader(csvFile222)
            nLine = 0
            for line in csv_reader:
                nLine = nLine + 1
                if nLine > 1:
                    pinyin = lazy_pinyin(line[1], style=Style.NORMAL)
                    email = ''.join(pinyin) + '@wangyuan.com'
                    line[4] = email
                    print(line[1], ''.join(pinyin), email)
                spamwriter.writerow([','.join(line)])

if __name__ == "__main__":
    main()