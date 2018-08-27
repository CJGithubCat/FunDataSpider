#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re

'''
Title  : 基金数据爬虫程序    
Date :   2018年8月26日
Version:  1.0
'''
class FundSipder(object):
    def __init__(self,url):
        self.url = url

    
    def printPage(self):
        print("开始打印{%s}的页面信息..." %(self.url))
        try:
            url = self.url
            req = urllib.request.Request(url)
            
            response = urllib.request.urlopen(req)
            html=response.read()
            gbk_html = html.decode('utf-8')
            
            print('*******************页面内容******************')
            print(gbk_html)
        except urllib.request.URLError as e:
            print(e.reason)
        
        


'''
*********************测试函数*********************
'''
if __name__ == '__main__':
    tempSider = FundSipder("http://fund.eastmoney.com/")
    tempSider.printPage()