'''
str2 = 'night'
str2.capitalize()
print(str2.capitalize())



def what():

    words = 6

    def whatinit():

        nonlocal words

        for i in range(10):
            for j in range(10):
                print(words+(i+j))

    return whatinit()


what()




g = lambda x: x*x+1

print(g(4))




g = list(filter(lambda x: x % 2, range(10)))

print(g)

print(list(map(lambda x: x + 2, range(10))))




def recursionA(n):

    if n == 1:

        return 1

    elif n == 2:

        return 1

    else:

        return recursionA(n-2)+recursionA(n-1)


print(recursionA(20))



dict4 = dict(((1, 'A'), (2, 'B'), (3, 'C')))

print(dict4[1])




file = open('/Users/gubaidan/Desktop/night.txt', 'r')

words = file.read(5)

print(words)

file.seek(0, 0)

print(file.readline())

file.seek(0, 0)

for i in file:
    print(i)




file = open('/Users/gubaidan/Desktop/night.txt', 'a')

file.write('shishi')



try:
    file = open('hello.txt')
    print(file.read())
    file.close()
except OSError as reason:
    print(str(reason))
except TypeError as reason:
    print(str(reason))



class AA:
    def __init__(self):
        print("构造函数init")

    def __new__(cls):
        print("new方法调用")

    def __delete__(self, instance):
        print("析gou函数调用")




class AA:
    def __str__(self):
        return "构造函数init"


a = AA()

print(a)


import time as time


def gettTme():
    t = time.localtime()
    l = str(t[0]) + '年' + str(t[1]) + '月' + str(t[2]) + "日   " + str(t[3]) + '：' + str(t[4]) + '：' + str(t[5])
    return l


print(gettTme())



class my:
    def __get__(self, instance, owner):
        print('get')

    def __set__(self, instance, value):
        print('set')

    def __delete__(self, instance):
        print("del")


class test:
    x = my()


t = test()

test.x

test.x = '   '

del test.x





def testList():

    x = [i for i in range(100) if not i % 2]

    return x


print(testList() )



string = "what the fuck"

x = iter(string)

print(next(x))

print(x.__next__())




class fibs:
    def __init__(self):
        self.a = 0
        self.b = 1

    def __iter__(self):

        return self

    def __next__(self):

        self.a, self.b = self.b, self.a + self.b
        return self.a


fibs = fibs()

print([x for x in fibs if x % 20])




def myGen():

    print("生成器")

    yield 1

    yield 2


my = myGen()



import requests

from bs4 import BeautifulSoup


res = requests.get('http://www.baidu.com/')

res.encoding = 'UTF-8'

soup = BeautifulSoup(res.text, 'html.parser')

aTag = soup.select('a')

listHref = [x['href'] for x in aTag]

listText = [y.text for y in aTag]

dictList = dict(zip(listText, listHref))


for i in dictList:
    print(i, dictList[i])




import requests

from bs4 import BeautifulSoup

import json

res = requests.get('http://120.79.48.71:8088/hrq/Activity/loadSearchPCTable?apartId=3&pageSize=10&pageTableNum=1&timeStart=1900-01-01&timeEnd=2100-01-01&listType=1')

res.encoding = 'UTF-8'


jd = json.loads(res.text)

for i in jd['rows']:
    print(i['setman'])
    print(i['remark'])





import requests

from bs4 import BeautifulSoup

res = requests.get('http://www.runoob.com/?s=%E6%AD%A3%E5%88%99')

res.encoding = 'UTF-8'

soup = BeautifulSoup(res.text, 'html.parser')


print(soup.select('.cate-list .sidebar-box a')[0].text)


listName = [x.text for x in soup.select('.cate-list .cate-items a')]

listContent = [y['href'] for y in soup.select('.cate-list .cate-items a')]

listTitle = [z['title'] for z in soup.select('.cate-list .cate-items a')]

dictList = dict(zip(listName, listContent,))


for index, i in enumerate(dictList):
    print(i, dictList[i], listTitle[index])


file = open('/Users/gubaidan/Desktop/night.txt', 'a')


try:

    for index, i in enumerate(dictList):
        file.write(str(index+1) + '、' + listName[index]+'\n')
        file.write(listContent[index]+'\n')
        file.write(listTitle[index] + '\n\n\n')

except OSError as reason:

    print(str(reason))

except TypeError as reason:

    print(str(reason))

'''


import requests

import json

import time

from bs4 import BeautifulSoup

import logging

import xlwt

# http://feed.mix.sina.com.cn/api/roll/get?pageid=87&lid=552&num=30&versionNumber=1.2.4&page=1&encode=utf-8&callback=feedCardJsonpCallback&_=1513141694459


# http://feed.mix.sina.com.cn/api/roll/get?pageid=87&lid=552&num=30&versionNumber=1.2.4&ctime=1513122688&encode=utf-8&callback=feedCardJsonpCallback&_=1513141733481


def getDate():

    floatTime = float(time.time())*1000

    r_index = str(floatTime).find('.')

    strTime = str(floatTime)[:r_index]

    return strTime


def getPreDate():

    cur_time = time.time()

    r_index = str(cur_time-cur_time % 86400).find('.')

    strTime = str(cur_time-cur_time % 86400)[:r_index]

    return strTime


def get_content_with_url(url):

    all_p = ''

    try:
        res = requests.get(url)

        res.encoding = 'utf-8'

        soup = BeautifulSoup(res.text, 'html.parser')

        for x in soup.select('#artibody p'):

            all_p += x.text

        return all_p

    except PermissionError as reason:

        logging.exception("")


def getContent(n):

    listTruple = []

    for inner in range(1, n):

        if 1:
            try:

                res = requests.get(
                    'http://feed.mix.sina.com.cn/api/roll/get?pageid=87&lid=552&num=30&versionNumber=1.2.4&page='+str(inner)
                    + '&encode=utf-8&callback=feedCardJsonpCallback&_='+getDate())

                res.encoding = 'unicode_escape'

                lIndex = res.text.find('{"result"')

                rIndex = res.text.find(');}catch(e){};')

                content = res.text[lIndex:rIndex].replace('"["', '"').replace('"]"', '"')

                jsonData = json.loads(content)

                for item in jsonData['result']['data']:

                    temp_content = get_content_with_url(item['url'])

                    list_temp = [item['title'], item['stitle'], item['summary'], item['intro'], item['keywords'],

                                  item['media_name'], item['ctime'], item['url'], temp_content]

                    listTruple.append(list_temp)

                # print(jsonData)

            except json.decoder.JSONDecodeError as reason:

                logging.exception("")

    return listTruple


def def_style():

    style = xlwt.XFStyle()

    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = 'True'
    font.size = 20
    style.font = font

    # 这部分设置居中格式
    alignment = xlwt.Alignment()

    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中

    alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中

    style.alignment = alignment

    return style


def main():

        try:

            workbook = xlwt.Workbook()

            sheet = workbook.add_sheet("sheet1", cell_overwrite_ok=True)

            style = def_style()

            sheet.write(0, 0, '新闻标题', style)

            sheet.write(0, 1, '副标题', style)

            sheet.write(0, 2, '简介', style)

            sheet.write(0, 3, '介绍', style)

            sheet.write(0, 4, '关键词', style)

            sheet.write(0, 5, '媒体名称', style)

            sheet.write(0, 6, '时间', style)

            sheet.write(0, 7, '链接', style)

            sheet.write(0, 8, '新闻内容', style)

            for index, item in enumerate(getContent(100)):

                sheet.write((index+1), 0, item[0])

                sheet.write((index+1), 1, item[1])

                sheet.write((index+1), 2, item[2])

                sheet.write((index+1), 3, item[3])

                sheet.write((index+1), 4, item[4])

                sheet.write((index+1), 5, item[5])

                sheet.write((index+1), 6, item[6])

                sheet.write((index+1), 7, item[7])

                sheet.write((index+1), 8, item[8])

            workbook.save('/Users/gubaidan/Desktop/news_list.xls')

            print('success')

        except OSError as reason:

            print(str(reason))

        except TypeError as reason:

            print(str(reason))


main()

