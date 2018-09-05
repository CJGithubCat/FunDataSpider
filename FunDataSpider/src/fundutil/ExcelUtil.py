#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Title  :     
Date :   2018年9月5日
Version:  1.0
'''
import xlrd
from spider.DBUtil import *
import urllib.request
import os

class ExcelUtil(object):
    
    def __init__(self):
        pass
      
    def readFile(self):
            querySql = "SELECT t.hangqingfilepath FROM t_index_new t WHERE t.hangqingzoushi IS NOT NULL ORDER BY t.index_code ASC LIMIT 0,1500"
            dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
            rows = dbUtil.query(querySql, None)
            count = 1
            for filePathT in rows:
                try:
                    #filePath = "C:/Users/CJ/Downloads/000300perf.xls"
                    filePath = filePathT[0]
                    print(filePath)
                    if filePath == "":
                        continue
                    else:
                        data = xlrd.open_workbook(filePath)        
                        sheet1 = "Price Return Index"
                        table = data.sheet_by_name(sheet1)
                        nrows =table.nrows
                        print(filePath)
                        rowIndex = 0
                        headers = table.row_values(rowIndex)
                        dataList = []
                        insertStr="INSERT INTO t_market_situation(info_date,index_code,index_sname,open_point,highest_point,lowest_point,close_point,rise_fall,rise_fall_range,deal_amount,deal_money,stock_member_num,pe1_ratio,pe2_ratio,dp1_ratio,dp2_ratio) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE date_update=now()"
                        
                        for rownum in range(1,nrows):
                            try:
                                row = table.row_values(rownum)
                                paramList = []
                                paramList.append(row[0])
                                paramList.append(row[1])
                                paramList.append(row[2])
                                paramList.append(row[6])
                                paramList.append(row[7])
                                paramList.append(row[8])
                                paramList.append(row[9])
                                paramList.append(row[10])
                                paramList.append(row[11])
                                paramList.append(row[12])
                                paramList.append(row[13])
                                paramList.append(row[14])
                                paramList.append(row[15])
                                paramList.append(row[16])
                                paramList.append(row[17])
                                paramList.append(row[18])
                                print(paramList)
                                dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
                                dbUtil.insert(insertStr,paramList)
                                
                            except Exception as e1:
                                pass
                            except ValueError as e2:
                                pass
                            except IOError as e3:
                                pass
                            except OSError:
                                pass
                            continue
                except Exception as e1:
                        pass
                except ValueError as e2:
                    pass
                except IOError as e3:
                    pass
                except OSError:
                    pass
                continue
            count = 1 +count
            print("count:%s" % count)
    
    def downLoadFile(self):
        querySql = "SELECT t.index_code,t.hangqingzoushi FROM t_index_new t WHERE t.hangqingzoushi IS NOT NULL ORDER BY t.index_code ASC LIMIT 0,1500"
        
        dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
        rows = dbUtil.query(querySql, None)
        count = 1
        updateSql = "UPDATE t_index_new set hangqingfilepath = '%s' WHERE index_code = '%s'"
        for row in rows:
            try:
                fileName = row[0]+".xls"            
                url = row[1]
                local = os.path.join('D:/pythontest/fund/hangqing',fileName)
                print(local)
                tempLoc = local.replace('\\',"/")
                upParm = (tempLoc,row[0])
                dbUtil.update(updateSql, upParm)
                #urllib.request.urlretrieve(url,local,None)
                count = count +1
                print("count:%s" % count)
            except Exception as e1:
                pass
            except ValueError as e2:
                pass
            except IOError as e3:
                pass
            except OSError:
                pass
            continue

if __name__=='__main__':
    excelUtil = ExcelUtil()
    excelUtil.readFile()
        
