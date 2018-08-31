#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Title  :  爬取天天基金首页内容   
Date :   2018年8月26日
Version:  1.0
'''
import urllib.request
from urllib import response
import re

class HomeSpider(object):    
    def __init__(self,url):
        self.url = url

    def parseContent(self,html,reg):
        try:
            pattern = re.compile(reg, re.S)
            items = pattern.findall(html)
            for item in items:
                print("item:%" % (item))
        except:
            print("ERR:parseContent is ERROR!")
    
    def loadPage(self):
        try:
            print("*****Start request URL:{%s}的页面..." % (self.url))
            #1.初始化参数            
            url = self.url            
            data = None
            head = {}
            head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            
            '''
                                如果有数据需要传，那么可以组装：
             data['type']='AUTO'                   
             data = urllib.parse.urlencode(data).encode("utf-8")
                              添加head信息另外一种方式：
             ##request.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
            '''
            #2.组装request请求
            request = urllib.request.Request(url,None,head)
            #3.发送请求并接受响应
            response = urllib.request.urlopen(request)
            html = response.read()
            #4.对页面数据解码为utf-8
            utf8html =html.decode('utf-8')
            #print("The Resp Html: %s" % (utf8html))
            print("解析制定内容")            
            #5.解析页面内容
            pattern = re.compile(r'<div class="content ui-text-gray-dark">(.*?)</div>', re.S)
            items = pattern.findall(utf8html)
            for item in items:
                print("item:%s" % (item))
                     
        except urllib.request.URLError as e:
            print("ERR:%s" % (e.reason))
    
if __name__ == '__main__':
    homeSipder =HomeSpider('http://fund.eastmoney.com/')
    homeSipder.loadPage()