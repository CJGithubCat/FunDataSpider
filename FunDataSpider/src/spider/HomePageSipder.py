#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re
from pyquery import PyQuery as pq
from lxml import etree
from spider.DBUtil import *

'''
Title  : 基金数据爬虫程序    
Date :   2018年8月26日
Version:  1.0
'''
class FundSipder(object):
    def __init__(self,url):
        self.url = url

    def reqPage(self,url):
        try:
            print("***开始请求{%s}的页面信息..." %(url))
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            html=response.read()
            utfhtml = html.decode('utf-8')
            return utfhtml            
        except urllib.request.URLError as e:
            print(e.reason)
        
    def parsePage(self,html,regStr):
        print("***开始解析{%s}的页面信息..." %(regStr))
        try:
            print('*******************页面内容******************')
           # print(html)
            doc = pq(html)            
            regDoc = doc(regStr)
            list = regDoc.items()
            reList = []
            for li in list:
                liQ = pq(li)
                itemDict = (liQ.text(),liQ.attr('href'))
                reList.append(itemDict)
            return reList
        except urllib.request.URLError as e:
            print(e.reason)
        
'''
*********************测试函数*********************
'''
if __name__ == '__main__':
    tempSider = FundSipder("http://fund.eastmoney.com/")
    
    itemDict={}
    #1.请求首页信息
    homePageHtml = tempSider.reqPage("http://fund.eastmoney.com/")
    regStr = '.jjsj .ui-text-gray-dark ul li a'
    reList = tempSider.parsePage(homePageHtml,regStr)
    print(reList)
    #2.将基金首页数据写入数据库
    dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
    #insertSql = "INSERT INTO t_website_info(item_name,item_url) VALUES(%s,%s)"    
    #dbUtil.insert(insertSql, reList)
    
    querySql = "select * from t_website_info"
    reList = dbUtil.query(querySql,None)
    print(reList)
    
    