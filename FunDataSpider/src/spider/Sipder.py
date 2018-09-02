#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re
from pyquery import PyQuery as pq
from lxml import etree
from spider.DBUtil import *

'''
Title  : 爬虫父类     
Date :   2018年9月1日
Version:  1.0
'''

class Spider(object):
    
    def __init__(self):
        pass

    def reqPage(self,url,charset):
        try:
            print("***开始请求{%s}的页面信息..." %(url))
            data = None
            headers = {}
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            req = urllib.request.Request(url,data,headers)
            response = urllib.request.urlopen(req)
            html=response.read()
            utfhtml = html.decode(charset,"ignore")
            return utfhtml            
        except urllib.request.URLError as e:
            print(e.reason)
    
    def parsePage(self,html,regStr):
        print("***开始解析{%s}的页面信息..." %(regStr))
        try:
            print('*******************页面内容******************')
            #print(html)
            doc = pq(html)            
            regDoc = doc(regStr)
            print(regDoc)
            list = regDoc.items()
            reList = []
            for li in list:
                liQ = pq(li)
                itemDict = (liQ.text(),liQ.attr('href'))
                reList.append(itemDict)
            return reList
        except urllib.request.URLError as e:
            print(e.reason)
    