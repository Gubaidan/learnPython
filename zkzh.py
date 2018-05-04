# -*- coding: utf-8 -*-
import requests
import random
import socket
import struct

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Referer': 'http://www.chsi.com.cn/cet',
    'X-FORWARDED-FOR':'',
	'CLIENT-IP':''
}

param={
        'zkzh':'',
        'xm':''}

param['xm']='顾振园' #单引号内修改为自己的姓名，例如param['xm']='张三'
xxdm = 420013 #学校代码，就是同校考试的同学准考证前六位，一样的
type = 2 #四级修改为1，六级修改为2
kc = 1 #考场默认从1开始，可以自行修改
zwh = 1 #座位号默认从1开始，可以自行修改
zwh_gd = 0 #已知座位号的请把0修改为1，并把上一行的1改为你的座位号

zkzh = (((xxdm*1000 + 172)*10+ type)*1000 + kc) * 100 + zwh #切勿修改此处
param['zkzh']=zkzh
print (param['zkzh'])

while 1:
    IP = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    HEADERS['X-FORWARDED-FOR'] = IP
    HEADERS['CLIENT-IP'] = IP
    try:
        rsp = requests.get('http://www.chsi.com.cn/cet/query',params=param, headers=HEADERS)
    except requests.exceptions.ConnectionError:
        continue
    except requests.exceptions.HTTPError:
        continue
    if '写作和翻译' in rsp.text:
        print(param['zkzh'], '查询成功')
        break
    else:
        print(param['zkzh'], '尝试失败')
        if zwh_gd:
            zkzh = zkzh + 100
        else:
            zkzh += 1
            temp = zkzh - 31
            if temp % 100 == 0:
                zkzh = zkzh + 70
        param['zkzh'] = zkzh
raw_input() 