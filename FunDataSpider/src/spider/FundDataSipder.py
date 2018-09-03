#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from spider.DBUtil import *
from pojo.TFundSummary import *
from pojo.TWebsiteInfo import *
from spider.Sipder import Spider
import demjson
import json
import time

class FundDataSpider(Spider):
    def __init__(self):
        pass
    
    def loadData(self,sql,paraList):
        try:
            dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
            #querySql = "select * from t_website_info"
            reList = dbUtil.query(sql,paraList)
            
            resultList = []
            for item in reList:
                websiteInfo = TWebsiteInfo(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])                
                resultList.append(websiteInfo)
            #print(resultList)
            return resultList
        except Exception as e:
            print(e.reason)
    def getFundInfo(self,resultList,item_name):
        websiteInfo ={}
        for result in resultList:
            #print(result.item_name)
            if result.item_name == item_name:
                #print(result.toString())
                websiteInfo = result
                break
        return websiteInfo
        #根据url获取页面并解析页面
            
    def parse1Level(self):
        fundDataSpider = FundDataSpider()
        sql= "select * from t_website_info"
        resultList = fundDataSpider.loadData(sql,None)
        websiteInfo = fundDataSpider.getFundInfo(resultList,"基金净值")
        print(websiteInfo.item_url)
        url=websiteInfo.item_url
        html = fundDataSpider.reqPage(url,'gb2312')
        
        regStr=".ul_l"
        reList = fundDataSpider.parsePage(html, regStr)
        print(reList)
        #2.将基金首页数据写入数据库
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        insertSql = "INSERT INTO t_website_info(item_name,item_url,level,parent_id) VALUES(%s,%s,2,8)"    
        dbUtil.insert(insertSql, reList)
        
    def parse2Level(self):
        fundDataSpider = FundDataSpider()
        sql= "select * from t_website_info"
        resultList = fundDataSpider.loadData(sql,None)
        websiteInfo = fundDataSpider.getFundInfo(resultList,"基金净值")
        print(websiteInfo.item_url)
        url=websiteInfo.item_url
        html = fundDataSpider.reqPage(url,'gb2312')
        #
        regStr="#tabtype li a"
        reList = fundDataSpider.parsePage(html, regStr)
        #2.将基金首页数据写入数据库
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        insertSql = "INSERT INTO t_website_info(item_name,item_url,level,parent_id) VALUES(%s,%s,3,33)"    
        dbUtil.insert(insertSql, reList)
    
    def getAllIndexInfo(self):       
        #1.查询数据库中所有的detatil_url
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        
        querySql40="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 440,10"
        querySql41="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 450,10"
        querySql42="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 460,10"
        querySql43="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 470,10"
        querySql44="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 480,10"
        querySql45="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 490,10"
        querySql46="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 500,10"
        querySql47="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 510,10"
        querySql48="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 520,10"
        querySql49="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 530,10"
        querySql50="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 540,10"
        querySql51="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 550,10"
        querySql52="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 560,10"
        querySql53="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 570,10"
        querySql54="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 580,10"
        querySql55="SELECT * FROM t_fund_summary ORDER BY fund_code DESC LIMIT 590,10"
        reList = dbUtil.query(querySql55, None)
        print(reList)
        regStr=".specialData"
        indexList = []
        count=1
        for data in reList:
            url=data[9]
            html=fundDataSpider.reqPage(url,'utf-8')        
            paList = fundDataSpider.parsePage(html, regStr)
            #print(paList[0][0])
            speStr = paList[0][0]
            indexInfo = ((speStr.split('|'))[0]).replace('跟踪标的：','')
            indexInfo = indexInfo.replace(' ','')
            indexList.append(indexInfo)
            print(count)
            count = count +1                       
        print(indexList)
        indexSet=set()
        for index in indexList:
            indexSet.add(index)
        #indexSet = (indexList)
        print('************插入数据库**************')
        print(indexSet) 
        insertSql = 'INSERT INTO t_index_info(index_name) VALUES(%s)';
        paramList=list(indexSet)
        print(paramList)
        dbUtil.insert(insertSql, paramList)
    
    def parseIndexFund(self):
        #2.加载页面
        url1='http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=5&letter=&gsid=&text=&sort=zdf,desc&page=1,9999&feature=|051&dt=1535817472944&atfc=&onlySale=0'
        url2='http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=5&letter=&gsid=&text=&sort=zdf,desc&page=1,9999&feature=|052&dt=1535817485442&atfc=&onlySale=0'
        html = fundDataSpider.reqPage(url2,'utf-8')
        reData = html.replace('var db=','')
        encodedjson = demjson.decode(reData)       
        indexData=encodedjson['datas']
        
        dataList = []
        for data in indexData:
            buyStatus = -1
            if data[9]=='开放申购':
                buyStatus = 1
            
            redemption_status=-1
            if data[9]=='开放赎回':
                redemption_status = 1
            
            poundage = data[17].replace('%','')
            if poundage == '' or poundage==None:
                poundage=0
            detail_url = 'http://fund.eastmoney.com/'+data[0]+'.html';
            fundSummary = TFundSummary(data[0],data[1],buyStatus,redemption_status,float(poundage),4,1,-1,-1,detail_url)            
            #print(detail_url)
            temTuople = (fundSummary.fund_code,fundSummary.fund_name,fundSummary.buy_status,fundSummary.redemption_status,fundSummary.poundage,fundSummary.fund_type,fundSummary.trace_type,fundSummary.trace_target,fundSummary.index_id,detail_url)
            dataList.append(temTuople)
        #3.插入到数据库
        print(dataList)
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        insertSql = "INSERT INTO t_fund_summary(fund_code,fund_name,buy_status,redemption_status,poundage,fund_type,trace_type,trace_target,index_id,detail_url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"    
        dbUtil.insert(insertSql, dataList)
    def updateIndex(self):
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        updateSql = "UPDATE t_index_info_1 SET stockCompany = %s WHERE id = %s"
        param =(1,6)
        dbUtil.update(updateSql, param)
    
    
    def loadCompanyInfo(self):
        commpanyInfos=[{
                        "id": "80000227",
                        "CompanyCode": "80000227",
                        "CompanyName": "长盛基金管理有限公司",
                        "SEARCHFIELD": "80000227长盛基金管理有限公司长盛基金CSJJ"
                    }, {
                        "id": "80000230",
                        "CompanyCode": "80000230",
                        "CompanyName": "鹏华基金管理有限公司",
                        "SEARCHFIELD": "80000230鹏华基金管理有限公司鹏华基金PHJJ"
                    }, {
                        "id": "80000223",
                        "CompanyCode": "80000223",
                        "CompanyName": "嘉实基金管理有限公司",
                        "SEARCHFIELD": "80000223嘉实基金管理有限公司嘉实基金JSJJ"
                    }, {
                        "id": "80000243",
                        "CompanyCode": "80000243",
                        "CompanyName": "长信基金管理有限责任公司",
                        "SEARCHFIELD": "80000243长信基金管理有限责任公司长信基金CXJJ"
                    }, {
                        "id": "80000095",
                        "CompanyCode": "80000095",
                        "CompanyName": "国都证券股份有限公司",
                        "SEARCHFIELD": "80000095国都证券股份有限公司国都证券GDZQ"
                    }, {
                        "id": "80065113",
                        "CompanyCode": "80065113",
                        "CompanyName": "中欧基金管理有限公司",
                        "SEARCHFIELD": "80065113中欧基金管理有限公司中欧基金ZOJJ"
                    }, {
                        "id": "80000225",
                        "CompanyCode": "80000225",
                        "CompanyName": "大成基金管理有限公司",
                        "SEARCHFIELD": "80000225大成基金管理有限公司大成基金DCJJ"
                    }, {
                        "id": "80000233",
                        "CompanyCode": "80000233",
                        "CompanyName": "国投瑞银基金管理有限公司",
                        "SEARCHFIELD": "80000233国投瑞银基金管理有限公司国投瑞银基金GTRYJJ"
                    }, {
                        "id": "80000250",
                        "CompanyCode": "80000250",
                        "CompanyName": "华宝基金管理有限公司",
                        "SEARCHFIELD": "80000250华宝基金管理有限公司华宝基金HBJJ"
                    }, {
                        "id": "80000237",
                        "CompanyCode": "80000237",
                        "CompanyName": "银河基金管理有限公司",
                        "SEARCHFIELD": "80000237银河基金管理有限公司银河基金YHJJ"
                    }, {
                        "id": "80000251",
                        "CompanyCode": "80000251",
                        "CompanyName": "景顺长城基金管理有限公司",
                        "SEARCHFIELD": "80000251景顺长城基金管理有限公司景顺长城基金JSCCJJ"
                    }, {
                        "id": "80048161",
                        "CompanyCode": "80048161",
                        "CompanyName": "东吴基金管理有限公司",
                        "SEARCHFIELD": "80048161东吴基金管理有限公司东吴基金DWJJ"
                    }, {
                        "id": "80000231",
                        "CompanyCode": "80000231",
                        "CompanyName": "融通基金管理有限公司",
                        "SEARCHFIELD": "80000231融通基金管理有限公司融通基金RTJJ"
                    }, {
                        "id": "80068180",
                        "CompanyCode": "80068180",
                        "CompanyName": "诺德基金管理有限公司",
                        "SEARCHFIELD": "80068180诺德基金管理有限公司诺德基金NDJJ"
                    }, {
                        "id": "80000224",
                        "CompanyCode": "80000224",
                        "CompanyName": "国泰基金管理有限公司",
                        "SEARCHFIELD": "80000224国泰基金管理有限公司国泰基金GTJJ"
                    }, {
                        "id": "80075936",
                        "CompanyCode": "80075936",
                        "CompanyName": "中邮基金管理股份有限公司",
                        "SEARCHFIELD": "80075936中邮创业基金管理股份有限公司中邮基金ZYJJ"
                    }, {
                        "id": "80086876",
                        "CompanyCode": "80086876",
                        "CompanyName": "金元顺安基金管理有限公司",
                        "SEARCHFIELD": "80086876金元顺安基金管理有限公司金元顺安基金JYSAJJ"
                    }, {
                        "id": "80139382",
                        "CompanyCode": "80139382",
                        "CompanyName": "长安基金管理有限公司",
                        "SEARCHFIELD": "80139382长安基金管理有限公司长安基金CAJJ"
                    }, {
                        "id": "80036742",
                        "CompanyCode": "80036742",
                        "CompanyName": "兴全基金管理有限公司",
                        "SEARCHFIELD": "80036742兴全基金管理有限公司兴全基金XQJJ"
                    }, {
                        "id": "80045188",
                        "CompanyCode": "80045188",
                        "CompanyName": "申万菱信基金管理有限公司",
                        "SEARCHFIELD": "80045188申万菱信基金管理有限公司申万菱信基金SWLXJJ"
                    }, {
                        "id": "80000222",
                        "CompanyCode": "80000222",
                        "CompanyName": "华夏基金管理有限公司",
                        "SEARCHFIELD": "80000222华夏基金管理有限公司华夏基金HXJJ"
                    }, {
                        "id": "80064225",
                        "CompanyCode": "80064225",
                        "CompanyName": "工银瑞信基金管理有限公司",
                        "SEARCHFIELD": "80064225工银瑞信基金管理有限公司工银瑞信基金GYRXJJ"
                    }, {
                        "id": "80092233",
                        "CompanyCode": "80092233",
                        "CompanyName": "农银汇理基金管理有限公司",
                        "SEARCHFIELD": "80092233农银汇理基金管理有限公司农银汇理基金NYHLJJ"
                    }, {
                        "id": "80000249",
                        "CompanyCode": "80000249",
                        "CompanyName": "新华基金管理有限公司",
                        "SEARCHFIELD": "80000249新华基金管理股份有限公司新华基金XHJJ"
                    }, {
                        "id": "80036782",
                        "CompanyCode": "80036782",
                        "CompanyName": "招商基金管理有限公司",
                        "SEARCHFIELD": "80036782招商基金管理有限公司招商基金ZSJJ"
                    }, {
                        "id": "80042861",
                        "CompanyCode": "80042861",
                        "CompanyName": "东方基金管理有限责任公司",
                        "SEARCHFIELD": "80042861东方基金管理有限责任公司东方基金DFJJ"
                    }, {
                        "id": "80000226",
                        "CompanyCode": "80000226",
                        "CompanyName": "博时基金管理有限公司",
                        "SEARCHFIELD": "80000226博时基金管理有限公司博时基金BSJJ"
                    }, {
                        "id": "80000080",
                        "CompanyCode": "80000080",
                        "CompanyName": "山西证券管理有限公司",
                        "SEARCHFIELD": "80000080山西证券股份有限公司山西证券SXZQ"
                    }, {
                        "id": "80048752",
                        "CompanyCode": "80048752",
                        "CompanyName": "中银基金管理有限公司",
                        "SEARCHFIELD": "80048752中银基金管理有限公司中银基金ZYJJ"
                    }, {
                        "id": "80000229",
                        "CompanyCode": "80000229",
                        "CompanyName": "易方达基金管理有限公司",
                        "SEARCHFIELD": "80000229易方达基金管理有限公司易方达基金YFDJJ"
                    }, {
                        "id": "80102419",
                        "CompanyCode": "80102419",
                        "CompanyName": "国金基金管理有限公司",
                        "SEARCHFIELD": "80102419国金基金管理有限公司国金基金GJJJ"
                    }, {
                        "id": "80000236",
                        "CompanyCode": "80000236",
                        "CompanyName": "宝盈基金管理有限公司",
                        "SEARCHFIELD": "80000236宝盈基金管理有限公司宝盈基金BYJJ"
                    }, {
                        "id": "80000245",
                        "CompanyCode": "80000245",
                        "CompanyName": "金鹰基金管理有限公司",
                        "SEARCHFIELD": "80000245金鹰基金管理有限公司金鹰基金JYJJ"
                    }, {
                        "id": "80041198",
                        "CompanyCode": "80041198",
                        "CompanyName": "天弘基金管理有限公司",
                        "SEARCHFIELD": "80041198天弘基金管理有限公司天弘基金THJJ"
                    }, {
                        "id": "80000240",
                        "CompanyCode": "80000240",
                        "CompanyName": "万家基金管理有限公司",
                        "SEARCHFIELD": "80000240万家基金管理有限公司万家基金WJJJ"
                    }, {
                        "id": "80046614",
                        "CompanyCode": "80046614",
                        "CompanyName": "中海基金管理有限公司",
                        "SEARCHFIELD": "80046614中海基金管理有限公司中海基金ZHJJ"
                    }, {
                        "id": "80000238",
                        "CompanyCode": "80000238",
                        "CompanyName": "泰达宏利基金管理有限公司",
                        "SEARCHFIELD": "80000238泰达宏利基金管理有限公司泰达宏利基金TDHLJJ"
                    }, {
                        "id": "80000239",
                        "CompanyCode": "80000239",
                        "CompanyName": "长城基金管理有限公司",
                        "SEARCHFIELD": "80000239长城基金管理有限公司长城基金CCJJ"
                    }, {
                        "id": "80050229",
                        "CompanyCode": "80050229",
                        "CompanyName": "上投摩根基金管理有限公司",
                        "SEARCHFIELD": "80050229上投摩根基金管理有限公司上投摩根基金STMGJJ"
                    }, {
                        "id": "80065990",
                        "CompanyCode": "80065990",
                        "CompanyName": "建信基金管理有限责任公司",
                        "SEARCHFIELD": "80065990建信基金管理有限责任公司建信基金JXJJ"
                    }, {
                        "id": "80053204",
                        "CompanyCode": "80053204",
                        "CompanyName": "华商基金管理有限公司",
                        "SEARCHFIELD": "80053204华商基金管理有限公司华商基金HSJJ"
                    }, {
                        "id": "80066470",
                        "CompanyCode": "80066470",
                        "CompanyName": "中信保诚基金管理有限公司",
                        "SEARCHFIELD": "80066470中信保诚基金管理有限公司中信保诚基金ZXBCJJ"
                    }, {
                        "id": "80092743",
                        "CompanyCode": "80092743",
                        "CompanyName": "华融证券管理有限公司",
                        "SEARCHFIELD": "80092743华融证券股份有限公司华融证券HRZQ"
                    }, {
                        "id": "80000246",
                        "CompanyCode": "80000246",
                        "CompanyName": "海富通基金管理有限公司",
                        "SEARCHFIELD": "80000246海富通基金管理有限公司海富通基金HFTJJ"
                    }, {
                        "id": "80043374",
                        "CompanyCode": "80043374",
                        "CompanyName": "国联安基金管理有限公司",
                        "SEARCHFIELD": "80043374国联安基金管理有限公司国联安基金GLAJJ"
                    }, {
                        "id": "80049689",
                        "CompanyCode": "80049689",
                        "CompanyName": "诺安基金管理有限公司",
                        "SEARCHFIELD": "80049689诺安基金管理有限公司诺安基金NAJJ"
                    }, {
                        "id": "80067635",
                        "CompanyCode": "80067635",
                        "CompanyName": "汇丰晋信基金管理有限公司",
                        "SEARCHFIELD": "80067635汇丰晋信基金管理有限公司汇丰晋信基金HFJXJJ"
                    }, {
                        "id": "80091787",
                        "CompanyCode": "80091787",
                        "CompanyName": "浦银安盛基金管理有限公司",
                        "SEARCHFIELD": "80091787浦银安盛基金管理有限公司浦银安盛基金PYASJJ"
                    }, {
                        "id": "80044515",
                        "CompanyCode": "80044515",
                        "CompanyName": "国海富兰克林基金管理有限公司",
                        "SEARCHFIELD": "80044515国海富兰克林基金管理有限公司国海富兰克林基金GHFLKLJJ"
                    }, {
                        "id": "80000235",
                        "CompanyCode": "80000235",
                        "CompanyName": "银华基金管理有限公司",
                        "SEARCHFIELD": "80000235银华基金管理股份有限公司银华基金YHJJ"
                    }, {
                        "id": "80064562",
                        "CompanyCode": "80064562管理有限公司",
                        "CompanyName": "交银施罗德基金",
                        "SEARCHFIELD": "80064562交银施罗德基金管理有限公司交银施罗德基金JYSLDJJ"
                    }, {
                        "id": "80000220",
                        "CompanyCode": "80000220",
                        "CompanyName": "南方基金管理有限公司",
                        "SEARCHFIELD": "80000220南方基金管理股份有限公司南方基金NFJJ"
                    }, {
                        "id": "80000221",
                        "CompanyCode": "80000221",
                        "CompanyName": "富国基金管理有限公司",
                        "SEARCHFIELD": "80000221富国基金管理有限公司富国基金FGJJ"
                    }, {
                        "id": "80036797",
                        "CompanyCode": "80036797",
                        "CompanyName": "摩根士丹利华鑫基金管理有限公司",
                        "SEARCHFIELD": "80036797摩根士丹利华鑫基金管理有限公司摩根士丹利华鑫基金MGSDLHXJJ"
                    }, {
                        "id": "80000248",
                        "CompanyCode": "80000248",
                        "CompanyName": "广发基金管理有限公司",
                        "SEARCHFIELD": "80000248广发基金管理有限公司广发基金GFJJ"
                    }, {
                        "id": "80000228",
                        "CompanyCode": "80000228",
                        "CompanyName": "华安基金管理有限公司",
                        "SEARCHFIELD": "80000228华安基金管理有限公司华安基金HAJJ"
                    }, {
                        "id": "80048088",
                        "CompanyCode": "80048088",
                        "CompanyName": "光大保德信基金管理有限公司",
                        "SEARCHFIELD": "80048088光大保德信基金管理有限公司光大保德信基金GDBDXJJ"
                    }, {
                        "id": "80053708",
                        "CompanyCode": "80053708",
                        "CompanyName": "汇添富基金管理股份有限公司",
                        "SEARCHFIELD": "80053708汇添富基金管理股份有限公司汇添富基金HTFJJ"
                    }, {
                        "id": "80055334",
                        "CompanyCode": "80055334",
                        "CompanyName": "华泰柏瑞基金管理有限公司",
                        "SEARCHFIELD": "80055334华泰柏瑞基金管理有限公司华泰柏瑞基金HTBRJJ"
                    }, {
                        "id": "80114781",
                        "CompanyCode": "80114781",
                        "CompanyName": "东兴证券股份有限公司",
                        "SEARCHFIELD": "80114781东兴证券股份有限公司东兴证券DXZQ"
                    }, {
                        "id": "80000252",
                        "CompanyCode": "80000252",
                        "CompanyName": "天治基金管理有限公司",
                        "SEARCHFIELD": "80000252天治基金管理有限公司天治基金TZJJ"
                    }, {
                        "id": "80074234",
                        "CompanyCode": "80074234",
                        "CompanyName": "信达澳银基金管理有限公司",
                        "SEARCHFIELD": "80074234信达澳银基金管理有限公司信达澳银基金XDAYJJ"
                    }, {
                        "id": "80106677",
                        "CompanyCode": "80106677",
                        "CompanyName": "民生加银基金管理有限公司",
                        "SEARCHFIELD": "80106677民生加银基金管理有限公司民生加银基金MSJYJJ"
                    }, {
                        "id": "80046522",
                        "CompanyCode": "80046522",
                        "CompanyName": "益民基金管理有限公司",
                        "SEARCHFIELD": "80046522益民基金管理有限公司益民基金YMJJ"
                    }, {
                        "id": "80000247",
                        "CompanyCode": "80000247",
                        "CompanyName": "泰信基金管理有限公司",
                        "SEARCHFIELD": "80000247泰信基金管理有限公司泰信基金TXJJ"
                    }, {
                        "id": "80037023",
                        "CompanyCode": "80037023",
                        "CompanyName": "华富基金管理有限公司",
                        "SEARCHFIELD": "80037023华富基金管理有限公司华富基金HFJJ"
                    }, {
                        "id": "80061674",
                        "CompanyCode": "80061674",
                        "CompanyName": "泰康资产管理有限责任公司",
                        "SEARCHFIELD": "80061674泰康资产管理有限责任公司泰康资产TKZC"
                    }, {
                        "id": "80128562",
                        "CompanyCode": "80128562",
                        "CompanyName": "富安达基金管理有限公司",
                        "SEARCHFIELD": "80128562富安达基金管理有限公司富安达基金FADJJ"
                    }, {
                        "id": "80175498",
                        "CompanyCode": "80175498",
                        "CompanyName": "英大基金管理有限公司",
                        "SEARCHFIELD": "80175498英大基金管理有限公司英大基金YDJJ"
                    }, {
                        "id": "80201857",
                        "CompanyCode": "80201857",
                        "CompanyName": "华宸未来基金管理有限公司",
                        "SEARCHFIELD": "80201857华宸未来基金管理有限公司华宸未来基金HCWLJJ"
                    }, {
                        "id": "80280036",
                        "CompanyCode": "80280036",
                        "CompanyName": "圆信永丰基金管理有限公司",
                        "SEARCHFIELD": "80280036圆信永丰基金管理有限公司圆信永丰基金YXYFJJ"
                    }, {
                        "id": "80455765",
                        "CompanyCode": "80455765",
                        "CompanyName": "中科沃土基金管理有限公司",
                        "SEARCHFIELD": "80455765中科沃土基金管理有限公司中科沃土基金ZKWTJJ"
                    }, {
                        "id": "80488954",
                        "CompanyCode": "80488954",
                        "CompanyName": "富荣基金管理有限公司",
                        "SEARCHFIELD": "80488954富荣基金管理有限公司富荣基金FRJJ"
                    }, {
                        "id": "80404004",
                        "CompanyCode": "80404004",
                        "CompanyName": "长江证券(上海)资产管理有限公司",
                        "SEARCHFIELD": "80404004长江证券(上海)资产管理有限公司长江证券(上海)CJZQSH"
                    }, {
                        "id": "80555446",
                        "CompanyCode": "80555446",
                        "CompanyName": "南华基金管理有限公司",
                        "SEARCHFIELD": "80555446南华基金管理有限公司南华基金NHJJ"
                    }, {
                        "id": "80145102",
                        "CompanyCode": "80145102",
                        "CompanyName": "上海东方证券资产管理管理有限公司",
                        "SEARCHFIELD": "80145102上海东方证券资产管理有限公司上海东方证券资产管理SHDFZQZCGL"
                    }, {
                        "id": "80168726",
                        "CompanyCode": "80168726",
                        "CompanyName": "平安大华基金管理有限公司",
                        "SEARCHFIELD": "80168726平安大华基金管理有限公司平安大华基金PADHJJ"
                    }, {
                        "id": "80161341",
                        "CompanyCode": "80161341",
                        "CompanyName": "财通基金管理有限公司",
                        "SEARCHFIELD": "80161341财通基金管理有限公司财通基金CTJJ"
                    }, {
                        "id": "80147736",
                        "CompanyCode": "80147736",
                        "CompanyName": "西部利得基金管理有限公司",
                        "SEARCHFIELD": "80147736西部利得基金管理有限公司西部利得基金XBLDJJ"
                    }, {
                        "id": "80355783",
                        "CompanyCode": "80355783",
                        "CompanyName": "国寿安保基金管理有限公司",
                        "SEARCHFIELD": "80355783国寿安保基金管理有限公司国寿安保基金GSABJJ"
                    }, {
                        "id": "80424273",
                        "CompanyCode": "80424273",
                        "CompanyName": "泓德基金管理有限公司",
                        "SEARCHFIELD": "80424273泓德基金管理有限公司泓德基金HDJJ"
                    }, {
                        "id": "80294346",
                        "CompanyCode": "80294346",
                        "CompanyName": "太平基金管理有限公司",
                        "SEARCHFIELD": "80294346太平基金管理有限公司太平基金TPJJ"
                    }, {
                        "id": "80498278",
                        "CompanyCode": "80498278",
                        "CompanyName": "汇安基金管理有限公司",
                        "SEARCHFIELD": "80498278汇安基金管理有限责任公司汇安基金HAJJ"
                    }, {
                        "id": "80056613",
                        "CompanyCode": "80056613",
                        "CompanyName": "高华证券管理有限公司",
                        "SEARCHFIELD": "80056613北京高华证券有限责任公司高华证券GHZQ"
                    }, {
                        "id": "80351991",
                        "CompanyCode": "80351991",
                        "CompanyName": "鑫元基金管理有限公司",
                        "SEARCHFIELD": "80351991鑫元基金管理有限公司鑫元基金XYJJ"
                    }, {
                        "id": "80501166",
                        "CompanyCode": "80501166",
                        "CompanyName": "先锋基金管理有限公司",
                        "SEARCHFIELD": "80501166先锋基金管理有限公司先锋基金XFJJ"
                    }, {
                        "id": "80508391",
                        "CompanyCode": "80508391",
                        "CompanyName": "中航基金管理有限公司",
                        "SEARCHFIELD": "80508391中航基金管理有限公司中航基金ZHJJ"
                    }, {
                        "id": "80000180",
                        "CompanyCode": "80000180",
                        "CompanyName": "渤海证券股份有限公司",
                        "SEARCHFIELD": "80000180渤海证券股份有限公司渤海证券BHZQ"
                    }, {
                        "id": "80366080",
                        "CompanyCode": "80366080",
                        "CompanyName": "上银基金管理有限公司",
                        "SEARCHFIELD": "80366080上银基金管理有限公司上银基金SYJJ"
                    }, {
                        "id": "80174741",
                        "CompanyCode": "80174741",
                        "CompanyName": "方正富邦基金管理有限公司",
                        "SEARCHFIELD": "80174741方正富邦基金管理有限公司方正富邦基金FZFBJJ"
                    }, {
                        "id": "80175511",
                        "CompanyCode": "80175511",
                        "CompanyName": "德邦基金管理有限公司",
                        "SEARCHFIELD": "80175511德邦基金管理有限公司德邦基金DBJJ"
                    }, {
                        "id": "80446423",
                        "CompanyCode": "80446423",
                        "CompanyName": "金信基金管理有限公司",
                        "SEARCHFIELD": "80446423金信基金管理有限公司金信基金JXJJ"
                    }, {
                        "id": "80205264",
                        "CompanyCode": "80205264",
                        "CompanyName": "江信基金管理有限公司",
                        "SEARCHFIELD": "80205264江信基金管理有限公司江信基金JXJJ"
                    }, {
                        "id": "80205263",
                        "CompanyCode": "80205263",
                        "CompanyName": "红塔红土管理有限公司",
                        "SEARCHFIELD": "80205263红塔红土基金管理有限公司红塔红土HTHT"
                    }, {
                        "id": "80380794",
                        "CompanyCode": "80380794",
                        "CompanyName": "创金合信基金管理有限公司",
                        "SEARCHFIELD": "80380794创金合信基金管理有限公司创金合信基金CJHXJJ"
                    }, {
                        "id": "80452130",
                        "CompanyCode": "80452130",
                        "CompanyName": "新沃基金管理有限公司",
                        "SEARCHFIELD": "80452130新沃基金管理有限公司新沃基金XWJJ"
                    }, {
                        "id": "80156777",
                        "CompanyCode": "80156777",
                        "CompanyName": "浙商基金管理有限公司",
                        "SEARCHFIELD": "80156777浙商基金管理有限公司浙商基金ZSJJ"
                    }, {
                        "id": "80163340",
                        "CompanyCode": "80163340",
                        "CompanyName": "安信基金管理有限公司",
                        "SEARCHFIELD": "80163340安信基金管理有限责任公司安信基金AXJJ"
                    }, {
                        "id": "80280395",
                        "CompanyCode": "80280395",
                        "CompanyName": "兴业基金管理有限公司",
                        "SEARCHFIELD": "80280395兴业基金管理有限公司兴业基金XYJJ"
                    }, {
                        "id": "80280039",
                        "CompanyCode": "80280039",
                        "CompanyName": "国开泰富基金管理有限责任公司",
                        "SEARCHFIELD": "80280039国开泰富基金管理有限责任公司国开泰富基金GKTFJJ"
                    }, {
                        "id": "80404701",
                        "CompanyCode": "80404701",
                        "CompanyName": "财通资管资产管理有限公司",
                        "SEARCHFIELD": "80404701财通证券资产管理有限公司财通资管CTZG"
                    }, {
                        "id": "80403111",
                        "CompanyCode": "80403111",
                        "CompanyName": "浙商证券资管理有限公司",
                        "SEARCHFIELD": "80403111浙江浙商证券资产管理有限公司浙商证券资管ZSZQZG"
                    }, {
                        "id": "80205268",
                        "CompanyCode": "80205268",
                        "CompanyName": "东海基金有限责任公司",
                        "SEARCHFIELD": "80205268东海基金管理有限责任公司东海基金DHJJ"
                    }, {
                        "id": "80355113",
                        "CompanyCode": "80355113",
                        "CompanyName": "中信建投基金管理有限公司",
                        "SEARCHFIELD": "80355113中信建投基金管理有限公司中信建投基金ZXJTJJ"
                    }, {
                        "id": "80356155",
                        "CompanyCode": "80356155",
                        "CompanyName": "永赢基金管理有限公司",
                        "SEARCHFIELD": "80356155永赢基金管理有限公司永赢基金YYJJ"
                    }, {
                        "id": "80280038",
                        "CompanyCode": "80280038",
                        "CompanyName": "前海开源基金管理有限公司",
                        "SEARCHFIELD": "80280038前海开源基金管理有限公司前海开源基金QHKYJJ"
                    }, {
                        "id": "80365985",
                        "CompanyCode": "80365985",
                        "CompanyName": "北信瑞丰管理有限公司",
                        "SEARCHFIELD": "80365985北信瑞丰基金管理有限公司北信瑞丰BXRF"
                    }, {
                        "id": "80365986",
                        "CompanyCode": "80365986",
                        "CompanyName": "中金基金管理有限公司",
                        "SEARCHFIELD": "80365986中金基金管理有限公司中金基金ZJJJ"
                    }, {
                        "id": "80548351",
                        "CompanyCode": "80548351",
                        "CompanyName": "格林基金管理有限公司",
                        "SEARCHFIELD": "80548351格林基金管理有限公司格林基金GLJJ"
                    }, {
                        "id": "80523667",
                        "CompanyCode": "80523667",
                        "CompanyName": "华泰保兴管理有限公司",
                        "SEARCHFIELD": "80523667华泰保兴基金管理有限公司华泰保兴HTBX"
                    }, {
                        "id": "80351345",
                        "CompanyCode": "80351345",
                        "CompanyName": "中加基金管理有限公司",
                        "SEARCHFIELD": "80351345中加基金管理有限公司中加基金ZJJJ"
                    }, {
                        "id": "80508384",
                        "CompanyCode": "80508384",
                        "CompanyName": "恒生前海基金管理有限公司",
                        "SEARCHFIELD": "80508384恒生前海基金管理有限公司恒生前海基金HSQHJJ"
                    }, {
                        "id": "80384640",
                        "CompanyCode": "80384640",
                        "CompanyName": "九泰基金管理有限公司",
                        "SEARCHFIELD": "80384640九泰基金管理有限公司九泰基金JTJJ"
                    }, {
                        "id": "80522693",
                        "CompanyCode": "80522693",
                        "CompanyName": "鹏扬基金管理有限公司",
                        "SEARCHFIELD": "80522693鹏扬基金管理有限公司鹏扬基金PYJJ"
                    }, {
                        "id": "80385906",
                        "CompanyCode": "80385906",
                        "CompanyName": "红土创新基金管理有限公司",
                        "SEARCHFIELD": "80385906红土创新基金管理有限公司红土创新基金HTCXJJ"
                    }, {
                        "id": "80199117",
                        "CompanyCode": "80199117",
                        "CompanyName": "华润元大基金管理有限公司",
                        "SEARCHFIELD": "80199117华润元大基金管理有限公司华润元大基金HRYDJJ"
                    }, {
                        "id": "80468996",
                        "CompanyCode": "80468996",
                        "CompanyName": "前海联合管理有限公司",
                        "SEARCHFIELD": "80468996新疆前海联合基金管理有限公司前海联合QHLH"
                    }, {
                        "id": "80341238",
                        "CompanyCode": "80341238",
                        "CompanyName": "中融基金管理有限公司",
                        "SEARCHFIELD": "80341238中融基金管理有限公司中融基金ZRJJ"
                    }, {
                        "id": "80365987",
                        "CompanyCode": "80365987",
                        "CompanyName": "嘉合基金管理有限公司",
                        "SEARCHFIELD": "80365987嘉合基金管理有限公司嘉合基金JHJJ"
                    }, {
                        "id": "80368700",
                        "CompanyCode": "80368700",
                        "CompanyName": "兴银基金管理有限责任公司",
                        "SEARCHFIELD": "80368700兴银基金管理有限责任公司兴银基金XYJJ"
                    }, {
                        "id": "80000200",
                        "CompanyCode": "80000200",
                        "CompanyName": "中银国际证券股份有限公司",
                        "SEARCHFIELD": "80000200中银国际证券股份有限公司中银国际证券ZYGJZQ"
                    }, {
                        "id": "80560381",
                        "CompanyCode": "80560381",
                        "CompanyName": "凯石基金管理有限公司",
                        "SEARCHFIELD": "80560381凯石基金管理有限公司凯石基金KSJJ"
                    }, {
                        "id": "80560389",
                        "CompanyCode": "80560389",
                        "CompanyName": "国融基金管理有限公司",
                        "SEARCHFIELD": "80560389国融基金管理有限公司国融基金GRJJ"
                    }, {
                        "id": "80560392",
                        "CompanyCode": "80560392",
                        "CompanyName": "博道基金管理有限公司",
                        "SEARCHFIELD": "80560392博道基金管理有限公司博道基金BDJJ"
                    }, {
                        "id": "80538609",
                        "CompanyCode": "80538609",
                        "CompanyName": "渤海汇金",
                        "SEARCHFIELD": "80538609渤海汇金证券资产管理有限公司渤海汇金BHHJ"
                    }, {
                        "id": "80391977",
                        "CompanyCode": "80391977",
                        "CompanyName": "华泰证券(上海)资产管理有限公司",
                        "SEARCHFIELD": "80391977华泰证券(上海)资产管理有限公司华泰证券(上海)HTZQSH"
                    }, {
                        "id": "80061431",
                        "CompanyCode": "80061431",
                        "CompanyName": "中国人保资产管理有限公司",
                        "SEARCHFIELD": "80061431中国人保资产管理有限公司人保资产RBZC"
                    }, {
                        "id": "80560388",
                        "CompanyCode": "80560388",
                        "CompanyName": "东方阿尔法基金管理有限公司",
                        "SEARCHFIELD": "80560388东方阿尔法基金管理有限公司东方阿尔法基金DFAEFJJ"
                    }, {
                        "id": "80560380",
                        "CompanyCode": "80560380",
                        "CompanyName": "恒越基金管理有限公司",
                        "SEARCHFIELD": "80560380恒越基金管理有限公司恒越基金HYJJ"
                    }, {
                        "id": "80560396",
                        "CompanyCode": "80560396",
                        "CompanyName": "合煦智远基金管理有限公司",
                        "SEARCHFIELD": "80560396合煦智远基金管理有限公司合煦智远基金HXZYJJ"
                    }, {
                        "id": "80560379",
                        "CompanyCode": "80560379",
                        "CompanyName": "弘毅远方基金管理有限公司",
                        "SEARCHFIELD": "80560379弘毅远方基金管理有限公司弘毅远方基金HYYFJJ"
                    }, {
                        "id": "80560393",
                        "CompanyCode": "80560393",
                        "CompanyName": "华融基金管理有限公司",
                        "SEARCHFIELD": "80560393华融基金管理有限公司华融基金HRJJ"
                    }, {
                        "id": "80560391",
                        "CompanyCode": "80560391",
                        "CompanyName": "中庚基金管理有限公司",
                        "SEARCHFIELD": "80560391中庚基金管理有限公司中庚基金ZGJJ"
                    }, {
                        "id": "80280397",
                        "CompanyCode": "80280397",
                        "CompanyName": "湘财基金管理有限公司",
                        "SEARCHFIELD": "80280397湘财基金管理有限公司湘财基金XCJJ"
                    }, {
                        "id": "80664536",
                        "CompanyCode": "80664536",
                        "CompanyName": "明亚基金管理有限责任公司",
                        "SEARCHFIELD": "80664536明亚基金管理有限责任公司明亚基金MYJJ"
                    }, {
                        "id": "80560383",
                        "CompanyCode": "80560383",
                        "CompanyName": "蜂巢基金管理有限公司",
                        "SEARCHFIELD": "80560383蜂巢基金管理有限公司蜂巢基金FCJJ"
                    }, {
                        "id": "80924817",
                        "CompanyCode": "80924817",
                        "CompanyName": "惠升基金管理有限责任公司",
                        "SEARCHFIELD": "80924817惠升基金管理有限责任公司惠升基金HSJJ"
                    }]
        paramList = []
        insertSql = "INSERT INTO t_company_info(id,company_code,company_name) VALUES(%s,%s,%s)"
        for company in commpanyInfos:
            print(company["id"])
            tempPa=(company["id"],company["CompanyCode"],company["CompanyName"])
            paramList.append(tempPa)
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        dbUtil.insert(insertSql, paramList)
    
    def updateIndexInfo(self):
        inexDict = {'沪深300指数':1,'上证380':2,'中证新兴产业指数':3,'深证基本面60指数':4,'恒生A股行业龙头指数':5,'深证300价值指数':6,'上证180公司治理指数':7,'上证成份指数':8,'沪深300价值指数':9,'中证腾安':10,'中证锐联基本面400指数':11,'责任指数':12,'上证港股通指数':13,'中信标普全债指数':14,'非周期':15,'中证内地低碳经济主题指数':16,'上证周期':17,'中证医疗指数':18,'上证50指数':19,'中证申万一带一路主题投资指数':20,'中证500等权重指数':21,'中证高铁产业指数':22,'中证国有企业红利指数':23,'恒生中国(香港上市)25指数':24,'中证10年期国开债指数':25,'中证政策性金融债1-3年指数':26,'中证政策性金融债8-10年指数':27,'恒生综合中型股指数':28,'中证中金优选300指数':29,'中证新能源汽车产业指数':30,'上证50AH优选人民币指数':31,'中证环境治理指数':32,'中证香港中小企业投资主题港元指数':33,'中信标普中国A股红利机会指数':34,'中证中药指数':35,'中证香港银行投资人民币指数':36,'中证申万证券行业指数':37,'中证生物科技主题指数':38,'国证航天军工指数':39,'中证能源互联网主题指数':40,'中证互联网医疗主题指数':41,'深证红利指数':42,'中证精准医疗主题指数':43,'中小板指数(价格)':44,'上证中小':45,'消费服务':46,'中证200指数':47,'上证180价值指数':48,'上证商品':49,'中小板300指数':50,'上证180成长指数':51,'深证民营指数':52,'消费80':53,'上证民企':54,'国证钢铁行业指数':55,'中证煤炭指数':56,'DowJonesChina88Index':57,'50等权':58,'中证基建工程指数':59,'中证方正富邦保险主题指数':60,'深证300价格':61,'中证锐联沪港深基本面100人民币指数':62,'中证智能家居指数':63,'中证TMT':64,'800医药':65,'央视财经50指数':66,'中证信息安全主题指数':67,'中证800金融':68,'中证800有色':69,'中证新能源指数':70,'中证互联网金融指数':71,'国证新能源指数':72,'中证健康产业指数':73,'中证100指数':74,'CSSW电子':75,'中证中航军工主题指数':76,'医药生物':77,'中证申万新兴健康产业主题投资指数':78,'沪深300等权重指数':79,'中证创业成长指数':80,'深证100指数(价格)':81,'中证500指数':82,'深证成份指数(价格)':83,'中小板综合指数':84,'中证可转换债券指数':85,'恒生香港35指数':86,'中证800等权重指数':87,'中证内地资源主题指数':88,'沪深300地产等权重指数':89,'国证生物医药指数':90,'中证白酒指数':91,'中证煤炭等权指数':92,'等权90':93,'沪深300高贝塔指数':94,'深证100指数(收益)':95,'中证人工智能主题指数':96,'中证大宗商品股票指数':97,'中证下游消费与服务产业指数':98,'CSWD并购':99,'中证上游资源产业指数':100,'中债新综合财富(总值)指数':101,'沪深300金融地产指数':102,'中证万得生物科技指数':103,'中证医药卫生指数':104,'中证娱乐主题指数':105,'中证体育产业指数':106,'中证工业4.0指数':107,'中证高端制造主题指数':108,'中证新能源汽车指数':109,'中证200指数':110,'中证军工指数':111,'中证空天一体军工指数':112,'中证锐联基本面50指数':113,'中证中期企业债指数':114,'中证一带一路主题指数':115,'中证环保产业指数':116,'中证国防指数':117,'中证800地产指数':118,'中证移动互联网指数':119,'中证银行指数':120,'中证酒':121,'A股资源':122,'中证信息技术指数':123,'创业板50指数':124,'中证定向增发事件指数':125,'中证800证券保险指数':126,'国证新能源汽车指数':127,'国证医药卫生行业指数':128,'国证有色金属行业指数':129,'国证食品饮料行业指数':130,'国证房地产行业指数':131,'中证50债券指数':132,'上证中盘':133,'中证互联网指数':134,'中证红利指数':135,'中小企业板创业板400指数':136,'上证资源':137,'深证成长40指数':138,'上证综合指数':139,'深证基本面200指数':140,'上证龙头':141,'上证180金融股指数':142,'上证超级大盘指数':143,'CHINAA':144,'中证金融地产指数':145,'MSCI中国A股国际通指数':146,'深证基本面120指数':147,'中华港股通精选100人民币指数':148,'中证复兴发展100主题指数':149,'中证京津冀协同发展主题指数':150,'中小企业板创业板400指数':151,'中债-1-3年农发行债券全价(总值)指数':152,'恒生港股通高股息低波动指数':153,'全指工业':154,'国证1000指数':155,'上证3-5年期中高等级可质押信用债指数':156,'CHINAAINTERNATIONAL':157,'国证2000指数':158,'创业板综合指数':159,'恒生中国企业指数':160,'国证A股指数':161,'富时A指':162,'中证10年期国开债指数':163,'中证红利低波动指数':164,'中证基建工程指数':165,'富时中国A50指数':166,'标普港股通低波红利指数':167,'中证全指家用电器指数':168,'中证全指汽车指数':169,'中证传媒指数':170,'巨潮100指数':171,'中证全指建筑材料指数':172,'中证港股通高股息精选人民币指数':173,'中证全指房地产指数':174,'中证智能消费主题指数':175,'深证电子信息传媒产业50指数':176,'中证银联智惠大数据100指数':177,'中证申万有色金属全收益指数':178,'中证1000指数':179,'中证南方小康产业指数':180,'中证全指证券公司指数':181,'中债国债总全价(7-10年)指数':182,'中债银华AAA信用债全价(总值)指数':183,'中证5年期地方政府债指数':184,'中证10年期地方政府债指数':185,'中债5年期国债期货期限匹配金融债全价(总值)指数':186,'中债10年期国债期货期限匹配金融债全价(总值)指数':187,'上证10年期国债指数':188,'上证5年期国债指数':189,'中证沪港深高股息精选人民币指数':190,'中债7-10年国开行债券全价(总值)指数':191,'中证转型成长指数':192,'中证兴业中高等级信用债指数':193,'中证500行业中性低波动指数':194,'中证财通中国可持续发展100(ECPIESG)指数':195,'中证上海国企指数':196,'上海清算所银行间0-1年中高等级信用债指数':197,'上海清算所银行间1-3年高等级信用债指数':198,'上海清算所银行间3-5年中高等级信用债指数':199,'上海清算所银行间1-3年中高等级信用债指数':200,'中证500信息技术指数':201,'全指金融':202,'全指信息':203,'中证养老产业指数':204,'黄金9999':205,'中证360互联网+大数据100指数':206,'中证社会发展安全产业主题指数':207,'中创100等权重指数':208,'中证食品饮料指数':209,'中证800指数':210,'创业板指数(价格)':211,'中证电子指数':212,'中证证券保险指数':213,'中证计算机指数':214,'中债国债总全价(3-5年)指数':215,'中证医药100指数':216,'大数据300指数':217,'中证TMT150指数':218,'中证精工制造指数':219,'沪深300医药卫生指数':220,'中证淘金大数据100指数':221,'全指医药':222,'iBoxx亚债中国指数':223,'全指可选':224,'中证大农业指数':225,'沪深300非银行金融指数':226,'沪深300安中动态策略指数':227,'中证细分医药产业主题全收益指数':228,'百发100指数':229,'中证主要消费指数':230,'中证金边中期国债指数':231,'沪深300非周期行业指数':232,'大数据100指数':233,'中证国有企业改革指数':234,'中证智能汽车主题指数':235,'中证港股通高股息投资人民币指数':236 }
        urlList = [
           
                    'http://fund.eastmoney.com/502053.html',
                    'http://fund.eastmoney.com/502056.html',
                    'http://fund.eastmoney.com/510080.html',
                    'http://fund.eastmoney.com/519027.html',
                    'http://fund.eastmoney.com/519032.html',
                    'http://fund.eastmoney.com/519034.html',
                    'http://fund.eastmoney.com/519100.html',
                    'http://fund.eastmoney.com/519116.html',
                    'http://fund.eastmoney.com/519117.html',
                    'http://fund.eastmoney.com/519180.html',
                    'http://fund.eastmoney.com/519300.html',
                    'http://fund.eastmoney.com/519671.html',
                    'http://fund.eastmoney.com/519677.html',
                    'http://fund.eastmoney.com/519686.html',
                    'http://fund.eastmoney.com/519706.html',
                    'http://fund.eastmoney.com/519931.html',
                    'http://fund.eastmoney.com/530010.html',
                    'http://fund.eastmoney.com/530015.html',
                    'http://fund.eastmoney.com/530018.html',
                    'http://fund.eastmoney.com/540012.html',
                    'http://fund.eastmoney.com/585001.html',
                    'http://fund.eastmoney.com/590007.html',
                    'http://fund.eastmoney.com/660008.html',
                    'http://fund.eastmoney.com/660011.html',
                    'http://fund.eastmoney.com/690008.html',
                    'http://fund.eastmoney.com/700002.html',
                    'http://fund.eastmoney.com/740101.html']
        urlDict = {'http://fund.eastmoney.com/000008.html':'000008',
                    'http://fund.eastmoney.com/000042.html':'000042',
                    'http://fund.eastmoney.com/000051.html':'000051',
                    'http://fund.eastmoney.com/000059.html':'000059',
                    'http://fund.eastmoney.com/000087.html':'000087',
                    'http://fund.eastmoney.com/000088.html':'000088',
                    'http://fund.eastmoney.com/000176.html':'000176',
                    'http://fund.eastmoney.com/000216.html':'000216',
                    'http://fund.eastmoney.com/000217.html':'000217',
                    'http://fund.eastmoney.com/000218.html':'000218',
                    'http://fund.eastmoney.com/000248.html':'000248',
                    'http://fund.eastmoney.com/000307.html':'000307',
                    'http://fund.eastmoney.com/000311.html':'000311',
                    'http://fund.eastmoney.com/000312.html':'000312',
                    'http://fund.eastmoney.com/000313.html':'000313',
                    'http://fund.eastmoney.com/000368.html':'000368',
                    'http://fund.eastmoney.com/000373.html':'000373',
                    'http://fund.eastmoney.com/000376.html':'000376',
                    'http://fund.eastmoney.com/000478.html':'000478',
                    'http://fund.eastmoney.com/000596.html':'000596',
                    'http://fund.eastmoney.com/000613.html':'000613',
                    'http://fund.eastmoney.com/000656.html':'000656',
                    'http://fund.eastmoney.com/000826.html':'000826',
                    'http://fund.eastmoney.com/000827.html':'000827',
                    'http://fund.eastmoney.com/000835.html':'000835',
                    'http://fund.eastmoney.com/000929.html':'000929',
                    'http://fund.eastmoney.com/000930.html':'000930',
                    'http://fund.eastmoney.com/000942.html':'000942',
                    'http://fund.eastmoney.com/000950.html':'000950',
                    'http://fund.eastmoney.com/000961.html':'000961',
                    'http://fund.eastmoney.com/000962.html':'000962',
                    'http://fund.eastmoney.com/000968.html':'000968',
                    'http://fund.eastmoney.com/000975.html':'000975',
                    'http://fund.eastmoney.com/001015.html':'001015',
                    'http://fund.eastmoney.com/001016.html':'001016',
                    'http://fund.eastmoney.com/001021.html':'001021',
                    'http://fund.eastmoney.com/001023.html':'001023',
                    'http://fund.eastmoney.com/001027.html':'001027',
                    'http://fund.eastmoney.com/001051.html':'001051',
                    'http://fund.eastmoney.com/001052.html':'001052',
                    'http://fund.eastmoney.com/001064.html':'001064',
                    'http://fund.eastmoney.com/001113.html':'001113',
                    'http://fund.eastmoney.com/001133.html':'001133',
                    'http://fund.eastmoney.com/001149.html':'001149',
                    'http://fund.eastmoney.com/001180.html':'001180',
                    'http://fund.eastmoney.com/001214.html':'001214',
                    'http://fund.eastmoney.com/001237.html':'001237',
                    'http://fund.eastmoney.com/001241.html':'001241',
                    'http://fund.eastmoney.com/001242.html':'001242',
                    'http://fund.eastmoney.com/001243.html':'001243',
                    'http://fund.eastmoney.com/001344.html':'001344',
                    'http://fund.eastmoney.com/001351.html':'001351',
                    'http://fund.eastmoney.com/001361.html':'001361',
                    'http://fund.eastmoney.com/001397.html':'001397',
                    'http://fund.eastmoney.com/001420.html':'001420',
                    'http://fund.eastmoney.com/001426.html':'001426',
                    'http://fund.eastmoney.com/001455.html':'001455',
                    'http://fund.eastmoney.com/001469.html':'001469',
                    'http://fund.eastmoney.com/001512.html':'001512',
                    'http://fund.eastmoney.com/001539.html':'001539',
                    'http://fund.eastmoney.com/001548.html':'001548',
                    'http://fund.eastmoney.com/001549.html':'001549',
                    'http://fund.eastmoney.com/001550.html':'001550',
                    'http://fund.eastmoney.com/001551.html':'001551',
                    'http://fund.eastmoney.com/001552.html':'001552',
                    'http://fund.eastmoney.com/001553.html':'001553',
                    'http://fund.eastmoney.com/001588.html':'001588',
                    'http://fund.eastmoney.com/001589.html':'001589',
                    'http://fund.eastmoney.com/001592.html':'001592',
                    'http://fund.eastmoney.com/001593.html':'001593',
                    'http://fund.eastmoney.com/001594.html':'001594',
                    'http://fund.eastmoney.com/001595.html':'001595',
                    'http://fund.eastmoney.com/001617.html':'001617',
                    'http://fund.eastmoney.com/001618.html':'001618',
                    'http://fund.eastmoney.com/001629.html':'001629',
                    'http://fund.eastmoney.com/001630.html':'001630',
                    'http://fund.eastmoney.com/001631.html':'001631',
                    'http://fund.eastmoney.com/001632.html':'001632',
                    'http://fund.eastmoney.com/001713.html':'001713',
                    'http://fund.eastmoney.com/001884.html':'001884',
                    'http://fund.eastmoney.com/001899.html':'001899',
                    'http://fund.eastmoney.com/002199.html':'002199',
                    'http://fund.eastmoney.com/002236.html':'002236',
                    'http://fund.eastmoney.com/002310.html':'002310',
                    'http://fund.eastmoney.com/002311.html':'002311',
                    'http://fund.eastmoney.com/002315.html':'002315',
                    'http://fund.eastmoney.com/002316.html':'002316',
                    'http://fund.eastmoney.com/002385.html':'002385',
                    'http://fund.eastmoney.com/002510.html':'002510',
                    'http://fund.eastmoney.com/002588.html':'002588',
                    'http://fund.eastmoney.com/002610.html':'002610',
                    'http://fund.eastmoney.com/002611.html':'002611',
                    'http://fund.eastmoney.com/002656.html':'002656',
                    'http://fund.eastmoney.com/002670.html':'002670',
                    'http://fund.eastmoney.com/002671.html':'002671',
                    'http://fund.eastmoney.com/002900.html':'002900',
                    'http://fund.eastmoney.com/002903.html':'002903',
                    'http://fund.eastmoney.com/002906.html':'002906',
                    'http://fund.eastmoney.com/002907.html':'002907',
                    'http://fund.eastmoney.com/002963.html':'002963',
                    'http://fund.eastmoney.com/002974.html':'002974',
                    'http://fund.eastmoney.com/002977.html':'002977',
                    'http://fund.eastmoney.com/002978.html':'002978',
                    'http://fund.eastmoney.com/002979.html':'002979',
                    'http://fund.eastmoney.com/002982.html':'002982',
                    'http://fund.eastmoney.com/002984.html':'002984',
                    'http://fund.eastmoney.com/002987.html':'002987',
                    'http://fund.eastmoney.com/003015.html':'003015',
                    'http://fund.eastmoney.com/003016.html':'003016',
                    'http://fund.eastmoney.com/003017.html':'003017',
                    'http://fund.eastmoney.com/003079.html':'003079',
                    'http://fund.eastmoney.com/003080.html':'003080',
                    'http://fund.eastmoney.com/003081.html':'003081',
                    'http://fund.eastmoney.com/003082.html':'003082',
                    'http://fund.eastmoney.com/003083.html':'003083',
                    'http://fund.eastmoney.com/003084.html':'003084',
                    'http://fund.eastmoney.com/003085.html':'003085',
                    'http://fund.eastmoney.com/003086.html':'003086',
                    'http://fund.eastmoney.com/003184.html':'003184',
                    'http://fund.eastmoney.com/003194.html':'003194',
                    'http://fund.eastmoney.com/003261.html':'003261',
                    'http://fund.eastmoney.com/003262.html':'003262',
                    'http://fund.eastmoney.com/003318.html':'003318',
                    'http://fund.eastmoney.com/003358.html':'003358',
                    'http://fund.eastmoney.com/003359.html':'003359',
                    'http://fund.eastmoney.com/003366.html':'003366',
                    'http://fund.eastmoney.com/003376.html':'003376',
                    'http://fund.eastmoney.com/003377.html':'003377',
                    'http://fund.eastmoney.com/003429.html':'003429',
                    'http://fund.eastmoney.com/003475.html':'003475',
                    'http://fund.eastmoney.com/003524.html':'003524',
                    'http://fund.eastmoney.com/003548.html':'003548',
                    'http://fund.eastmoney.com/003578.html':'003578',
                    'http://fund.eastmoney.com/003579.html':'003579',
                    'http://fund.eastmoney.com/003646.html':'003646',
                    'http://fund.eastmoney.com/003647.html':'003647',
                    'http://fund.eastmoney.com/003702.html':'003702',
                    'http://fund.eastmoney.com/003765.html':'003765',
                    'http://fund.eastmoney.com/003766.html':'003766',
                    'http://fund.eastmoney.com/003814.html':'003814',
                    'http://fund.eastmoney.com/003815.html':'003815',
                    'http://fund.eastmoney.com/003817.html':'003817',
                    'http://fund.eastmoney.com/003818.html':'003818',
                    'http://fund.eastmoney.com/003876.html':'003876',
                    'http://fund.eastmoney.com/003884.html':'003884',
                    'http://fund.eastmoney.com/003885.html':'003885',
                    'http://fund.eastmoney.com/003932.html':'003932',
                    'http://fund.eastmoney.com/003933.html':'003933',
                    'http://fund.eastmoney.com/003934.html':'003934',
                    'http://fund.eastmoney.com/003935.html':'003935',
                    'http://fund.eastmoney.com/003986.html':'003986',
                    'http://fund.eastmoney.com/003987.html':'003987',
                    'http://fund.eastmoney.com/003988.html':'003988',
                    'http://fund.eastmoney.com/003989.html':'003989',
                    'http://fund.eastmoney.com/003990.html':'003990',
                    'http://fund.eastmoney.com/003995.html':'003995',
                    'http://fund.eastmoney.com/003996.html':'003996',
                    'http://fund.eastmoney.com/004069.html':'004069',
                    'http://fund.eastmoney.com/004070.html':'004070',
                    'http://fund.eastmoney.com/004085.html':'004085',
                    'http://fund.eastmoney.com/004086.html':'004086',
                    'http://fund.eastmoney.com/004190.html':'004190',
                    'http://fund.eastmoney.com/004191.html':'004191',
                    'http://fund.eastmoney.com/004192.html':'004192',
                    'http://fund.eastmoney.com/004193.html':'004193',
                    'http://fund.eastmoney.com/004194.html':'004194',
                    'http://fund.eastmoney.com/004195.html':'004195',
                    'http://fund.eastmoney.com/004253.html':'004253',
                    'http://fund.eastmoney.com/004342.html':'004342',
                    'http://fund.eastmoney.com/004343.html':'004343',
                    'http://fund.eastmoney.com/004344.html':'004344',
                    'http://fund.eastmoney.com/004345.html':'004345',
                    'http://fund.eastmoney.com/004346.html':'004346',
                    'http://fund.eastmoney.com/004347.html':'004347',
                    'http://fund.eastmoney.com/004348.html':'004348',
                    'http://fund.eastmoney.com/004354.html':'004354',
                    'http://fund.eastmoney.com/004407.html':'004407',
                    'http://fund.eastmoney.com/004408.html':'004408',
                    'http://fund.eastmoney.com/004409.html':'004409',
                    'http://fund.eastmoney.com/004410.html':'004410',
                    'http://fund.eastmoney.com/004416.html':'004416',
                    'http://fund.eastmoney.com/004432.html':'004432',
                    'http://fund.eastmoney.com/004433.html':'004433',
                    'http://fund.eastmoney.com/004488.html':'004488',
                    'http://fund.eastmoney.com/004532.html':'004532',
                    'http://fund.eastmoney.com/004533.html':'004533',
                    'http://fund.eastmoney.com/004593.html':'004593',
                    'http://fund.eastmoney.com/004597.html':'004597',
                    'http://fund.eastmoney.com/004598.html':'004598',
                    'http://fund.eastmoney.com/004642.html':'004642',
                    'http://fund.eastmoney.com/004643.html':'004643',
                    'http://fund.eastmoney.com/004742.html':'004742',
                    'http://fund.eastmoney.com/004743.html':'004743',
                    'http://fund.eastmoney.com/004744.html':'004744',
                    'http://fund.eastmoney.com/004746.html':'004746',
                    'http://fund.eastmoney.com/004752.html':'004752',
                    'http://fund.eastmoney.com/004753.html':'004753',
                    'http://fund.eastmoney.com/004854.html':'004854',
                    'http://fund.eastmoney.com/004855.html':'004855',
                    'http://fund.eastmoney.com/004856.html':'004856',
                    'http://fund.eastmoney.com/004857.html':'004857',
                    'http://fund.eastmoney.com/004870.html':'004870',
                    'http://fund.eastmoney.com/004874.html':'004874',
                    'http://fund.eastmoney.com/004875.html':'004875',
                    'http://fund.eastmoney.com/004876.html':'004876',
                    'http://fund.eastmoney.com/004945.html':'004945',
                    'http://fund.eastmoney.com/004996.html':'004996',
                    'http://fund.eastmoney.com/005051.html':'005051',
                    'http://fund.eastmoney.com/005052.html':'005052',
                    'http://fund.eastmoney.com/005062.html':'005062',
                    'http://fund.eastmoney.com/005063.html':'005063',
                    'http://fund.eastmoney.com/005064.html':'005064',
                    'http://fund.eastmoney.com/005093.html':'005093',
                    'http://fund.eastmoney.com/005112.html':'005112',
                    'http://fund.eastmoney.com/005113.html':'005113',
                    'http://fund.eastmoney.com/005114.html':'005114',
                    'http://fund.eastmoney.com/005125.html':'005125',
                    'http://fund.eastmoney.com/005152.html':'005152',
                    'http://fund.eastmoney.com/005183.html':'005183',
                    'http://fund.eastmoney.com/005223.html':'005223',
                    'http://fund.eastmoney.com/005224.html':'005224',
                    'http://fund.eastmoney.com/005229.html':'005229',
                    'http://fund.eastmoney.com/005279.html':'005279',
                    'http://fund.eastmoney.com/005285.html':'005285',
                    'http://fund.eastmoney.com/005287.html':'005287',
                    'http://fund.eastmoney.com/005288.html':'005288',
                    'http://fund.eastmoney.com/005339.html':'005339',
                    'http://fund.eastmoney.com/005390.html':'005390',
                    'http://fund.eastmoney.com/005391.html':'005391',
                    'http://fund.eastmoney.com/005414.html':'005414',
                    'http://fund.eastmoney.com/005415.html':'005415',
                    'http://fund.eastmoney.com/005554.html':'005554',
                    'http://fund.eastmoney.com/005555.html':'005555',
                    'http://fund.eastmoney.com/005561.html':'005561',
                    'http://fund.eastmoney.com/005562.html':'005562',
                    'http://fund.eastmoney.com/005563.html':'005563',
                    'http://fund.eastmoney.com/005564.html':'005564',
                    'http://fund.eastmoney.com/005565.html':'005565',
                    'http://fund.eastmoney.com/005566.html':'005566',
                    'http://fund.eastmoney.com/005567.html':'005567',
                    'http://fund.eastmoney.com/005568.html':'005568',
                    'http://fund.eastmoney.com/005581.html':'005581',
                    'http://fund.eastmoney.com/005582.html':'005582',
                    'http://fund.eastmoney.com/005607.html':'005607',
                    'http://fund.eastmoney.com/005608.html':'005608',
                    'http://fund.eastmoney.com/005623.html':'005623',
                    'http://fund.eastmoney.com/005624.html':'005624',
                    'http://fund.eastmoney.com/005633.html':'005633',
                    'http://fund.eastmoney.com/005639.html':'005639',
                    'http://fund.eastmoney.com/005640.html':'005640',
                    'http://fund.eastmoney.com/005658.html':'005658',
                    'http://fund.eastmoney.com/005691.html':'005691',
                    'http://fund.eastmoney.com/005692.html':'005692',
                    'http://fund.eastmoney.com/005693.html':'005693',
                    'http://fund.eastmoney.com/005702.html':'005702',
                    'http://fund.eastmoney.com/005727.html':'005727',
                    'http://fund.eastmoney.com/005733.html':'005733',
                    'http://fund.eastmoney.com/005735.html':'005735',
                    'http://fund.eastmoney.com/005737.html':'005737',
                    'http://fund.eastmoney.com/005761.html':'005761',
                    'http://fund.eastmoney.com/005762.html':'005762',
                    'http://fund.eastmoney.com/005788.html':'005788',
                    'http://fund.eastmoney.com/005789.html':'005789',
                    'http://fund.eastmoney.com/005795.html':'005795',
                    'http://fund.eastmoney.com/005803.html':'005803',
                    'http://fund.eastmoney.com/005804.html':'005804',
                    'http://fund.eastmoney.com/005807.html':'005807',
                    'http://fund.eastmoney.com/005808.html':'005808',
                    'http://fund.eastmoney.com/005813.html':'005813',
                    'http://fund.eastmoney.com/005814.html':'005814',
                    'http://fund.eastmoney.com/005829.html':'005829',
                    'http://fund.eastmoney.com/005830.html':'005830',
                    'http://fund.eastmoney.com/005832.html':'005832',
                    'http://fund.eastmoney.com/005867.html':'005867',
                    'http://fund.eastmoney.com/005868.html':'005868',
                    'http://fund.eastmoney.com/005869.html':'005869',
                    'http://fund.eastmoney.com/005870.html':'005870',
                    'http://fund.eastmoney.com/005873.html':'005873',
                    'http://fund.eastmoney.com/005874.html':'005874',
                    'http://fund.eastmoney.com/005918.html':'005918',
                    'http://fund.eastmoney.com/005919.html':'005919',
                    'http://fund.eastmoney.com/005994.html':'005994',
                    'http://fund.eastmoney.com/005998.html':'005998',
                    'http://fund.eastmoney.com/005999.html':'005999',
                    'http://fund.eastmoney.com/006020.html':'006020',
                    'http://fund.eastmoney.com/006021.html':'006021',
                    'http://fund.eastmoney.com/006048.html':'006048',
                    'http://fund.eastmoney.com/006063.html':'006063',
                    'http://fund.eastmoney.com/006087.html':'006087',
                    'http://fund.eastmoney.com/006098.html':'006098',
                    'http://fund.eastmoney.com/006131.html':'006131',
                    'http://fund.eastmoney.com/006248.html':'006248',
                    'http://fund.eastmoney.com/006249.html':'006249',
                    'http://fund.eastmoney.com/006262.html':'006262',
                    'http://fund.eastmoney.com/006355.html':'006355',
                    'http://fund.eastmoney.com/020011.html':'020011',
                    'http://fund.eastmoney.com/020021.html':'020021',
                    'http://fund.eastmoney.com/020035.html':'020035',
                    'http://fund.eastmoney.com/020036.html':'020036',
                    'http://fund.eastmoney.com/040002.html':'040002',
                    'http://fund.eastmoney.com/040180.html':'040180',
                    'http://fund.eastmoney.com/040190.html':'040190',
                    'http://fund.eastmoney.com/050002.html':'050002',
                    'http://fund.eastmoney.com/050013.html':'050013',
                    'http://fund.eastmoney.com/050021.html':'050021',
                    'http://fund.eastmoney.com/050024.html':'050024',
                    'http://fund.eastmoney.com/070023.html':'070023',
                    'http://fund.eastmoney.com/070030.html':'070030',
                    'http://fund.eastmoney.com/090010.html':'090010',
                    'http://fund.eastmoney.com/090012.html':'090012',
                    'http://fund.eastmoney.com/100032.html':'100032',
                    'http://fund.eastmoney.com/100038.html':'100038',
                    'http://fund.eastmoney.com/100053.html':'100053',
                    'http://fund.eastmoney.com/110003.html':'110003',
                    'http://fund.eastmoney.com/110019.html':'110019',
                    'http://fund.eastmoney.com/110020.html':'110020',
                    'http://fund.eastmoney.com/110021.html':'110021',
                    'http://fund.eastmoney.com/110026.html':'110026',
                    'http://fund.eastmoney.com/110030.html':'110030',
                    'http://fund.eastmoney.com/160119.html':'160119',
                    'http://fund.eastmoney.com/160123.html':'160123',
                    'http://fund.eastmoney.com/160124.html':'160124',
                    'http://fund.eastmoney.com/160135.html':'160135',
                    'http://fund.eastmoney.com/160136.html':'160136',
                    'http://fund.eastmoney.com/160137.html':'160137',
                    'http://fund.eastmoney.com/160218.html':'160218',
                    'http://fund.eastmoney.com/160219.html':'160219',
                    'http://fund.eastmoney.com/160221.html':'160221',
                    'http://fund.eastmoney.com/160222.html':'160222',
                    'http://fund.eastmoney.com/160223.html':'160223',
                    'http://fund.eastmoney.com/160224.html':'160224',
                    'http://fund.eastmoney.com/160225.html':'160225',
                    'http://fund.eastmoney.com/160415.html':'160415',
                    'http://fund.eastmoney.com/160417.html':'160417',
                    'http://fund.eastmoney.com/160418.html':'160418',
                    'http://fund.eastmoney.com/160419.html':'160419',
                    'http://fund.eastmoney.com/160420.html':'160420',
                    'http://fund.eastmoney.com/160422.html':'160422',
                    'http://fund.eastmoney.com/160516.html':'160516',
                    'http://fund.eastmoney.com/160517.html':'160517',
                    'http://fund.eastmoney.com/160615.html':'160615',
                    'http://fund.eastmoney.com/160616.html':'160616',
                    'http://fund.eastmoney.com/160620.html':'160620',
                    'http://fund.eastmoney.com/160625.html':'160625',
                    'http://fund.eastmoney.com/160626.html':'160626',
                    'http://fund.eastmoney.com/160628.html':'160628',
                    'http://fund.eastmoney.com/160629.html':'160629',
                    'http://fund.eastmoney.com/160630.html':'160630',
                    'http://fund.eastmoney.com/160631.html':'160631',
                    'http://fund.eastmoney.com/160632.html':'160632',
                    'http://fund.eastmoney.com/160633.html':'160633',
                    'http://fund.eastmoney.com/160634.html':'160634',
                    'http://fund.eastmoney.com/160635.html':'160635',
                    'http://fund.eastmoney.com/160636.html':'160636',
                    'http://fund.eastmoney.com/160637.html':'160637',
                    'http://fund.eastmoney.com/160638.html':'160638',
                    'http://fund.eastmoney.com/160639.html':'160639',
                    'http://fund.eastmoney.com/160640.html':'160640',
                    'http://fund.eastmoney.com/160643.html':'160643',
                    'http://fund.eastmoney.com/160706.html':'160706',
                    'http://fund.eastmoney.com/160716.html':'160716',
                    'http://fund.eastmoney.com/160720.html':'160720',
                    'http://fund.eastmoney.com/160721.html':'160721',
                    'http://fund.eastmoney.com/160724.html':'160724',
                    'http://fund.eastmoney.com/160725.html':'160725',
                    'http://fund.eastmoney.com/160806.html':'160806',
                    'http://fund.eastmoney.com/160807.html':'160807',
                    'http://fund.eastmoney.com/160808.html':'160808',
                    'http://fund.eastmoney.com/160814.html':'160814',
                    'http://fund.eastmoney.com/161017.html':'161017',
                    'http://fund.eastmoney.com/161022.html':'161022',
                    'http://fund.eastmoney.com/161024.html':'161024',
                    'http://fund.eastmoney.com/161025.html':'161025',
                    'http://fund.eastmoney.com/161026.html':'161026',
                    'http://fund.eastmoney.com/161027.html':'161027',
                    'http://fund.eastmoney.com/161028.html':'161028',
                    'http://fund.eastmoney.com/161029.html':'161029',
                    'http://fund.eastmoney.com/161030.html':'161030',
                    'http://fund.eastmoney.com/161031.html':'161031',
                    'http://fund.eastmoney.com/161032.html':'161032',
                    'http://fund.eastmoney.com/161033.html':'161033',
                    'http://fund.eastmoney.com/161035.html':'161035',
                    'http://fund.eastmoney.com/161036.html':'161036',
                    'http://fund.eastmoney.com/161037.html':'161037',
                    'http://fund.eastmoney.com/161039.html':'161039',
                    'http://fund.eastmoney.com/161118.html':'161118',
                    'http://fund.eastmoney.com/161119.html':'161119',
                    'http://fund.eastmoney.com/161120.html':'161120',
                    'http://fund.eastmoney.com/161121.html':'161121',
                    'http://fund.eastmoney.com/161122.html':'161122',
                    'http://fund.eastmoney.com/161123.html':'161123',
                    'http://fund.eastmoney.com/161207.html':'161207',
                    'http://fund.eastmoney.com/161211.html':'161211',
                    'http://fund.eastmoney.com/161213.html':'161213',
                    'http://fund.eastmoney.com/161217.html':'161217',
                    'http://fund.eastmoney.com/161223.html':'161223',
                    'http://fund.eastmoney.com/161227.html':'161227',
                    'http://fund.eastmoney.com/161604.html':'161604',
                    'http://fund.eastmoney.com/161607.html':'161607',
                    'http://fund.eastmoney.com/161612.html':'161612',
                    'http://fund.eastmoney.com/161613.html':'161613',
                    'http://fund.eastmoney.com/161628.html':'161628',
                    'http://fund.eastmoney.com/161629.html':'161629',
                    'http://fund.eastmoney.com/161631.html':'161631',
                    'http://fund.eastmoney.com/161715.html':'161715',
                    'http://fund.eastmoney.com/161718.html':'161718',
                    'http://fund.eastmoney.com/161720.html':'161720',
                    'http://fund.eastmoney.com/161721.html':'161721',
                    'http://fund.eastmoney.com/161723.html':'161723',
                    'http://fund.eastmoney.com/161724.html':'161724',
                    'http://fund.eastmoney.com/161725.html':'161725',
                    'http://fund.eastmoney.com/161726.html':'161726',
                    'http://fund.eastmoney.com/161811.html':'161811',
                    'http://fund.eastmoney.com/161812.html':'161812',
                    'http://fund.eastmoney.com/161816.html':'161816',
                    'http://fund.eastmoney.com/161819.html':'161819',
                    'http://fund.eastmoney.com/161825.html':'161825',
                    'http://fund.eastmoney.com/161826.html':'161826',
                    'http://fund.eastmoney.com/161907.html':'161907',
                    'http://fund.eastmoney.com/162213.html':'162213',
                    'http://fund.eastmoney.com/162216.html':'162216',
                    'http://fund.eastmoney.com/162307.html':'162307',
                    'http://fund.eastmoney.com/162412.html':'162412',
                    'http://fund.eastmoney.com/162413.html':'162413',
                    'http://fund.eastmoney.com/162416.html':'162416',
                    'http://fund.eastmoney.com/162509.html':'162509',
                    'http://fund.eastmoney.com/162510.html':'162510',
                    'http://fund.eastmoney.com/162711.html':'162711',
                    'http://fund.eastmoney.com/162714.html':'162714',
                    'http://fund.eastmoney.com/162907.html':'162907',
                    'http://fund.eastmoney.com/163109.html':'163109',
                    'http://fund.eastmoney.com/163111.html':'163111',
                    'http://fund.eastmoney.com/163113.html':'163113',
                    'http://fund.eastmoney.com/163114.html':'163114',
                    'http://fund.eastmoney.com/163115.html':'163115',
                    'http://fund.eastmoney.com/163116.html':'163116',
                    'http://fund.eastmoney.com/163118.html':'163118',
                    'http://fund.eastmoney.com/163119.html':'163119',
                    'http://fund.eastmoney.com/163209.html':'163209',
                    'http://fund.eastmoney.com/163407.html':'163407',
                    'http://fund.eastmoney.com/163808.html':'163808',
                    'http://fund.eastmoney.com/163821.html':'163821',
                    'http://fund.eastmoney.com/164304.html':'164304',
                    'http://fund.eastmoney.com/164401.html':'164401',
                    'http://fund.eastmoney.com/164402.html':'164402',
                    'http://fund.eastmoney.com/164508.html':'164508',
                    'http://fund.eastmoney.com/164809.html':'164809',
                    'http://fund.eastmoney.com/164811.html':'164811',
                    'http://fund.eastmoney.com/164818.html':'164818',
                    'http://fund.eastmoney.com/164819.html':'164819',
                    'http://fund.eastmoney.com/164820.html':'164820',
                    'http://fund.eastmoney.com/164821.html':'164821',
                    'http://fund.eastmoney.com/164825.html':'164825',
                    'http://fund.eastmoney.com/164905.html':'164905',
                    'http://fund.eastmoney.com/164907.html':'164907',
                    'http://fund.eastmoney.com/164908.html':'164908',
                    'http://fund.eastmoney.com/165309.html':'165309',
                    'http://fund.eastmoney.com/165312.html':'165312',
                    'http://fund.eastmoney.com/165511.html':'165511',
                    'http://fund.eastmoney.com/165515.html':'165515',
                    'http://fund.eastmoney.com/165519.html':'165519',
                    'http://fund.eastmoney.com/165520.html':'165520',
                    'http://fund.eastmoney.com/165521.html':'165521',
                    'http://fund.eastmoney.com/165522.html':'165522',
                    'http://fund.eastmoney.com/165523.html':'165523',
                    'http://fund.eastmoney.com/165524.html':'165524',
                    'http://fund.eastmoney.com/165525.html':'165525',
                    'http://fund.eastmoney.com/165707.html':'165707',
                    'http://fund.eastmoney.com/165806.html':'165806',
                    'http://fund.eastmoney.com/165809.html':'165809',
                    'http://fund.eastmoney.com/165810.html':'165810',
                    'http://fund.eastmoney.com/166007.html':'166007',
                    'http://fund.eastmoney.com/166402.html':'166402',
                    'http://fund.eastmoney.com/166802.html':'166802',
                    'http://fund.eastmoney.com/167301.html':'167301',
                    'http://fund.eastmoney.com/167503.html':'167503',
                    'http://fund.eastmoney.com/167601.html':'167601',
                    'http://fund.eastmoney.com/168001.html':'168001',
                    'http://fund.eastmoney.com/168201.html':'168201',
                    'http://fund.eastmoney.com/168203.html':'168203',
                    'http://fund.eastmoney.com/168204.html':'168204',
                    'http://fund.eastmoney.com/168205.html':'168205',
                    'http://fund.eastmoney.com/180003.html':'180003',
                    'http://fund.eastmoney.com/180033.html':'180033',
                    'http://fund.eastmoney.com/200002.html':'200002',
                    'http://fund.eastmoney.com/202015.html':'202015',
                    'http://fund.eastmoney.com/202017.html':'202017',
                    'http://fund.eastmoney.com/202021.html':'202021',
                    'http://fund.eastmoney.com/202025.html':'202025',
                    'http://fund.eastmoney.com/202211.html':'202211',
                    'http://fund.eastmoney.com/206005.html':'206005',
                    'http://fund.eastmoney.com/206010.html':'206010',
                    'http://fund.eastmoney.com/213010.html':'213010',
                    'http://fund.eastmoney.com/217016.html':'217016',
                    'http://fund.eastmoney.com/217017.html':'217017',
                    'http://fund.eastmoney.com/217019.html':'217019',
                    'http://fund.eastmoney.com/217027.html':'217027',
                    'http://fund.eastmoney.com/233010.html':'233010',
                    'http://fund.eastmoney.com/240014.html':'240014',
                    'http://fund.eastmoney.com/240016.html':'240016',
                    'http://fund.eastmoney.com/240019.html':'240019',
                    'http://fund.eastmoney.com/257060.html':'257060',
                    'http://fund.eastmoney.com/270010.html':'270010',
                    'http://fund.eastmoney.com/270026.html':'270026',
                    'http://fund.eastmoney.com/290010.html':'290010',
                    'http://fund.eastmoney.com/310318.html':'310318',
                    'http://fund.eastmoney.com/310398.html':'310398',
                    'http://fund.eastmoney.com/320010.html':'320010',
                    'http://fund.eastmoney.com/320014.html':'320014',
                    'http://fund.eastmoney.com/370023.html':'370023',
                    'http://fund.eastmoney.com/399001.html':'399001',
                    'http://fund.eastmoney.com/410008.html':'410008',
                    'http://fund.eastmoney.com/410010.html':'410010',
                    'http://fund.eastmoney.com/450008.html':'450008',
                    'http://fund.eastmoney.com/460220.html':'460220',
                    'http://fund.eastmoney.com/460300.html':'460300',
                    'http://fund.eastmoney.com/470007.html':'470007',
                    'http://fund.eastmoney.com/470068.html':'470068',
                    'http://fund.eastmoney.com/481009.html':'481009',
                    'http://fund.eastmoney.com/481012.html':'481012',
                    'http://fund.eastmoney.com/501002.html':'501002',
                    'http://fund.eastmoney.com/501005.html':'501005',
                    'http://fund.eastmoney.com/501006.html':'501006',
                    'http://fund.eastmoney.com/501007.html':'501007',
                    'http://fund.eastmoney.com/501008.html':'501008',
                    'http://fund.eastmoney.com/501009.html':'501009',
                    'http://fund.eastmoney.com/501010.html':'501010',
                    'http://fund.eastmoney.com/501011.html':'501011',
                    'http://fund.eastmoney.com/501012.html':'501012',
                    'http://fund.eastmoney.com/501016.html':'501016',
                    'http://fund.eastmoney.com/501019.html':'501019',
                    'http://fund.eastmoney.com/501023.html':'501023',
                    'http://fund.eastmoney.com/501025.html':'501025',
                    'http://fund.eastmoney.com/501029.html':'501029',
                    'http://fund.eastmoney.com/501030.html':'501030',
                    'http://fund.eastmoney.com/501031.html':'501031',
                    'http://fund.eastmoney.com/501036.html':'501036',
                    'http://fund.eastmoney.com/501037.html':'501037',
                    'http://fund.eastmoney.com/501043.html':'501043',
                    'http://fund.eastmoney.com/501045.html':'501045',
                    'http://fund.eastmoney.com/501047.html':'501047',
                    'http://fund.eastmoney.com/501048.html':'501048',
                    'http://fund.eastmoney.com/501050.html':'501050',
                    'http://fund.eastmoney.com/501057.html':'501057',
                    'http://fund.eastmoney.com/501058.html':'501058',
                    'http://fund.eastmoney.com/501059.html':'501059',
                    'http://fund.eastmoney.com/501060.html':'501060',
                    'http://fund.eastmoney.com/501061.html':'501061',
                    'http://fund.eastmoney.com/501101.html':'501101',
                    'http://fund.eastmoney.com/501105.html':'501105',
                    'http://fund.eastmoney.com/501106.html':'501106',
                    'http://fund.eastmoney.com/501301.html':'501301',
                    'http://fund.eastmoney.com/501303.html':'501303',
                    'http://fund.eastmoney.com/501305.html':'501305',
                    'http://fund.eastmoney.com/501306.html':'501306',
                    'http://fund.eastmoney.com/501307.html':'501307',
                    'http://fund.eastmoney.com/501308.html':'501308',
                    'http://fund.eastmoney.com/502000.html':'502000',
                    'http://fund.eastmoney.com/502003.html':'502003',
                    'http://fund.eastmoney.com/502006.html':'502006',
                    'http://fund.eastmoney.com/502010.html':'502010',
                    'http://fund.eastmoney.com/502013.html':'502013',
                    'http://fund.eastmoney.com/502020.html':'502020',
                    'http://fund.eastmoney.com/502023.html':'502023',
                    'http://fund.eastmoney.com/502030.html':'502030',
                    'http://fund.eastmoney.com/502036.html':'502036',
                    'http://fund.eastmoney.com/502040.html':'502040',
                    'http://fund.eastmoney.com/502048.html':'502048',
                    'http://fund.eastmoney.com/502053.html':'502053',
                    'http://fund.eastmoney.com/502056.html':'502056',
                    'http://fund.eastmoney.com/510080.html':'510080',
                    'http://fund.eastmoney.com/519027.html':'519027',
                    'http://fund.eastmoney.com/519032.html':'519032',
                    'http://fund.eastmoney.com/519034.html':'519034',
                    'http://fund.eastmoney.com/519100.html':'519100',
                    'http://fund.eastmoney.com/519116.html':'519116',
                    'http://fund.eastmoney.com/519117.html':'519117',
                    'http://fund.eastmoney.com/519180.html':'519180',
                    'http://fund.eastmoney.com/519300.html':'519300',
                    'http://fund.eastmoney.com/519671.html':'519671',
                    'http://fund.eastmoney.com/519677.html':'519677',
                    'http://fund.eastmoney.com/519686.html':'519686',
                    'http://fund.eastmoney.com/519706.html':'519706',
                    'http://fund.eastmoney.com/519931.html':'519931',
                    'http://fund.eastmoney.com/530010.html':'530010',
                    'http://fund.eastmoney.com/530015.html':'530015',
                    'http://fund.eastmoney.com/530018.html':'530018',
                    'http://fund.eastmoney.com/540012.html':'540012',
                    'http://fund.eastmoney.com/585001.html':'585001',
                    'http://fund.eastmoney.com/590007.html':'590007',
                    'http://fund.eastmoney.com/660008.html':'660008',
                    'http://fund.eastmoney.com/660011.html':'660011',
                    'http://fund.eastmoney.com/690008.html':'690008',
                    'http://fund.eastmoney.com/700002.html':'700002',
                    'http://fund.eastmoney.com/740101.html':'740101'}
        
        regStr=".specialData"
        for urlInfo in urlList:
            #print(urlDict[urlInfo])            
            html=fundDataSpider.reqPage(urlInfo,'utf-8')        
            paList = fundDataSpider.parsePage(html, regStr)
            #print(paList[0][0])
            speStr = paList[0][0]
            indexInfo = ((speStr.split('|'))[0]).replace('跟踪标的：','')
            indexInfo = indexInfo.replace(' ','')
            fundCode = urlDict[urlInfo]
            inexId = inexDict[indexInfo]
            
            dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
            updateSql = "UPDATE t_fund_summary SET index_id = %s WHERE fund_code = %s"
            data =(inexId,fundCode)
            print(data)            
            dbUtil.update(updateSql, data)
            time.sleep(1)
                    
    
if __name__=='__main__':
    fundDataSpider = FundDataSpider()
    fundDataSpider.loadCompanyInfo();