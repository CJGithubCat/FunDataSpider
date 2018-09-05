#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from spider.DBUtil import *
from pojo.TFundSummary import *
from pojo.TWebsiteInfo import *
from spider.Sipder import Spider
import demjson
import json
import time

class IndexCodeSpider(Spider):
    
    def __init__(self):
        pass

    def getIndexInfo(self):
        querySql = "SELECT index_name FROM t_index_info"
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        reRows = dbUtil.query(querySql, None)
        print(reRows)
        
        for row in reRows:
            indexName = row[0]
            url = 'http://www.csindex.com.cn/zh-CN/search/indices?key='+indexName
            print(url)
            html = indexSpider.reqPage(url, "utf-8")
            #print(html)
            
            regStr="#itemContainer tr td a"
            paList = indexSpider.parsePage(html, regStr)
            updateStr = "UPDATE t_index_info set index_code = '%s' WHERE index_name = '%s'"
            if len(paList) > 0:
                upParam =(paList[0][0],indexName)
                print(upParam)            
                dbUtil.update(updateStr, upParam)
            
    def getNullIndexCode(self):
        querySql = "SELECT t.`fund_name`,t.`detail_url` FROM t_fund_summary t WHERE t.`index_code` IS NULL"
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        reRows = dbUtil.query(querySql, None)
        #print(reRows)
        
        regStr=".specialData"
        insertqq = "INSERT INTO t_temp_info(detail_url,some_index_name,remark) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE remark =''"
        detail_url=['http://fund.eastmoney.com/000216.html',
#'http://fund.eastmoney.com/005567.html',
#'http://fund.eastmoney.com/005568.html',
#'http://fund.eastmoney.com/180003.html',
'http://fund.eastmoney.com/202017.html',
'http://fund.eastmoney.com/206010.html',
'http://fund.eastmoney.com/217016.html',
'http://fund.eastmoney.com/217019.html',
'http://fund.eastmoney.com/233010.html',
'http://fund.eastmoney.com/270026.html',
'http://fund.eastmoney.com/310398.html',
'http://fund.eastmoney.com/410010.html',
'http://fund.eastmoney.com/470068.html',
'http://fund.eastmoney.com/481012.html',
'http://fund.eastmoney.com/501019.html',
'http://fund.eastmoney.com/501023.html',
'http://fund.eastmoney.com/501025.html',
'http://fund.eastmoney.com/501029.html',
'http://fund.eastmoney.com/501050.html',
'http://fund.eastmoney.com/501301.html',
'http://fund.eastmoney.com/501303.html',
'http://fund.eastmoney.com/501305.html',
'http://fund.eastmoney.com/501306.html',
'http://fund.eastmoney.com/501307.html',
'http://fund.eastmoney.com/501308.html',
'http://fund.eastmoney.com/502023.html',
'http://fund.eastmoney.com/510080.html',
'http://fund.eastmoney.com/519180.html',
'http://fund.eastmoney.com/519671.html',
'http://fund.eastmoney.com/519677.html',
'http://fund.eastmoney.com/519706.html',
'http://fund.eastmoney.com/530018.html',
'http://fund.eastmoney.com/540012.html',
'http://fund.eastmoney.com/700002.html']
        
        for item in detail_url:
            url = item
            print(url)
            html = indexSpider.reqPage(url, "utf-8")
            paList = indexSpider.parsePage(html, regStr)
            if len(paList) > 0:
                speStr = paList[0][0]
                indexInfo = ((speStr.split('|'))[0]).replace('跟踪标的：','')
                ppLi = []
                ppLi.append(url)
                ppLi.append(indexInfo)
                
                indexInfo = indexInfo.replace('CHINA A','')
                indexInfo = indexInfo.replace('中证财通中国可持续发展100(ECPI ESG)指数','')
                qqurl = 'http://www.csindex.com.cn/zh-CN/search/indices?key='+indexInfo
                qqHtml = indexSpider.reqPage(qqurl, "utf-8")
                regStrqq="#itemContainer tr td a"
                paList = indexSpider.parsePage(qqHtml, regStrqq)
                upParam = "  "
                if len(paList) > 0:
                    upParam =paList[0][0]
                    print(upParam) 
                ppLi.append(upParam)
                dbUtil.insert(insertqq,ppLi)
if __name__=='__main__':
    indexSpider = IndexCodeSpider()
    indexSpider.getNullIndexCode()
