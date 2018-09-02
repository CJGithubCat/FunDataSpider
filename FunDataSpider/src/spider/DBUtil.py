#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql

class DBUtil(object):
    def __init__(self,host,port,username,password,dbname,charset='utf-8'):
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.dbname=dbname
        self.charset=charset    
    '''
            函数功能:新增数据
    '''    
    def insert(self,sql,list):
        try:
            conn = pymysql.connect(host=self.host,port=self.port,user=self.username,passwd=self.password,db=self.dbname,charset='utf8')
            cursor = conn.cursor()
            cursor.executemany(sql,list)
            conn.commit()
            cursor.close()
            conn.close()
        except pymysql.err.Error as e:
            print(e)
                
    def query(self,sql,list):
        try:            
            conn = pymysql.connect(host=self.host,port=self.port,user=self.username,passwd=self.password,db=self.dbname)
            cursor = conn.cursor()
            cursor.execute(sql,list)
            #获取查询结果
            rows = cursor.fetchall()
            
            conn.commit()
            cursor.close()
            conn.close()
            return rows
        except pymysql.err.Error as e:
            print(e)
    
    def update(self,sql,data):
        try:
            conn = pymysql.connect(host=self.host,port=self.port,user=self.username,passwd=self.password,db=self.dbname,charset='utf8')
            cursor = conn.cursor()
            cursor.execute(sql % data)
            conn.commit()
            cursor.close()
            conn.close()
        except pymysql.err.Error as e:
            print(e)
          
if __name__=="__main__":
    dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
    sql="INSERT INTO t_website_info(item_name,item_url) VALUES(%s,%s)";
    list=[("B","22"),("C","33")]
    dbUtil.insert(sql, list)
    
    #querySql = "select * from t_website_info"
    #dbUtil.query(querySql,None)
    