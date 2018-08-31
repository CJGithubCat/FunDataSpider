#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from spider.DBUtil import *

class FundDataSpider(object):
    def __init__(self):
        pass
    
    def loadPage(self):
        try:
            dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
            querySql = "select * from t_website_info"
            reList = dbUtil.query(querySql,None)
            print(reList)
            for item in 
            
            
        except Exception as e:
            print(e.reason)


if __name__=='__main__':
    