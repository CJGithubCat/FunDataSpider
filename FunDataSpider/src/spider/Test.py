#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Title  :     
Date :   2018年9月1日
Version:  1.0
'''
from spider.Sipder import Spider

class Test(Spider):
    
    def __init__(self):
        pass
    
    

if __name__ == '__main__':
    tempSider = Test()
    itemDict={}
    #1.请求首页信息
    homePageHtml = tempSider.reqPage("http://fund.eastmoney.com/")
    regStr = '.jjsj .ui-text-gray-dark ul li a'
    reList = tempSider.parsePage(homePageHtml,regStr)
    print(reList)
    
    