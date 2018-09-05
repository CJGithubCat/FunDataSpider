#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spider.DBUtil import *
from pojo.TFundSummary import *
from pojo.TWebsiteInfo import *
from spider.Sipder import Spider
import demjson
import json
import time

class IndexInfoSipder(Spider):
    
    def __init__(self):
        pass
    
    def getIndexInfo(self):
        dict = {
    "total": 6,
    "page_size": "30",
    "total_page": 2,
    "list": [
        [
            {
                "index_id": 289,
                "index_code": "399701",
                "indx_sname": "深证F60",
                "index_ename": "SZFI 60",
                "base_point": "1000.0000",
                "base_date": "2002-12-31 00:00:00",
                "online_date": "2010-05-10",
                "is_custom": 0,
                "is_show": 1,
                "index_c_intro": "深证基本面60指数以深市A股为样本空间，分别挑选基本面价值最大的60家上市公司作为样本。基本面价值由四个财务指标来衡量，并决定了样本股的权重。",
                "index_e_intro": "SZFI 60 Index consists of top 60 SZSE-listed stocks ranked by fundamental value, which is calculated by 4 financial factors (Revenue, Cash Flow, Book Value and Dividends). And the weights of constituents are also decided by the fundamental value rather than the capitalization. ",
                "class_series": 3,
                "class_region": 7,
                "class_assets": 10,
                "class_classify": 21,
                "class_currency": 22,
                "class_hot": 25,
                "index_c_fullname": "深证基本面60指数",
                "index_e_fullname": "SZFI 60 Index",
                "created_at": "2017-07-03 14:00:02",
                "updated_at": "2017-07-03 14:00:02",
                "classes": {
                    "class_id": 3,
                    "class_type": 1,
                    "class_name": "深证系列指数",
                    "class_ename": "SZSE Indices",
                    "created_at": "2017-03-29 20:12:15",
                    "updated_at": "2017-03-29 20:12:23"
                },
                "files": [
                    {
                        "file_id": 1308,
                        "file_title": "编制方案",
                        "file_name": "289_399701_Index_Methodology_cn.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 1,
                        "index_id": 289,
                        "created_at": "2017-07-06 17:17:27",
                        "updated_at": "2017-07-06 17:17:27"
                    },
                    {
                        "file_id": 2825,
                        "file_title": "指数单张",
                        "file_name": "399701factsheet.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 2,
                        "index_id": 289,
                        "created_at": "2018-09-03 17:22:44",
                        "updated_at": "2018-09-03 17:22:44"
                    }
                ]
            },
            "http://www.csindex.com.cn/uploads/file/autofile/perf/399701perf.xls",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/289_399701_Index_Methodology_cn.pdf",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/CSIMeth.pdf",
            "http://www.csindex.com.cn/uploads/file/autofile/cons/399701cons.xls",
            ""
        ],
        [
            {
                "index_id": 290,
                "index_code": "399702",
                "indx_sname": "深证F120",
                "index_ename": "SZFI 120",
                "base_point": "1000.0000",
                "base_date": "2002-12-31 00:00:00",
                "online_date": "2010-05-10",
                "is_custom": 0,
                "is_show": 1,
                "index_c_intro": "深证基本面120指数以深市A股为样本空间，分别挑选基本面价值最大的120家上市公司作为样本。基本面价值由四个财务指标来衡量，并决定了样本股的权重。",
                "index_e_intro": "SZFI 120 Index consists of top 120 SZSE-listed stocks ranked by fundamental value, which is calculated by 4 financial factors (Revenue, Cash Flow, Book Value and Dividends). And the weights of constituents are also decided by the fundamental value rather than the capitalization. ",
                "class_series": 3,
                "class_region": 7,
                "class_assets": 10,
                "class_classify": 21,
                "class_currency": 22,
                "class_hot": 25,
                "index_c_fullname": "深证基本面120指数",
                "index_e_fullname": "SZFI 120 Index",
                "created_at": "2017-07-03 14:00:02",
                "updated_at": "2017-07-03 14:00:02",
                "classes": {
                    "class_id": 3,
                    "class_type": 1,
                    "class_name": "深证系列指数",
                    "class_ename": "SZSE Indices",
                    "created_at": "2017-03-29 20:12:15",
                    "updated_at": "2017-03-29 20:12:23"
                },
                "files": [
                    {
                        "file_id": 1310,
                        "file_title": "编制方案",
                        "file_name": "290_399702_Index_Methodology_cn.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 1,
                        "index_id": 290,
                        "created_at": "2017-07-06 17:17:27",
                        "updated_at": "2017-07-06 17:17:27"
                    },
                    {
                        "file_id": 2827,
                        "file_title": "指数单张",
                        "file_name": "399702factsheet.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 2,
                        "index_id": 290,
                        "created_at": "2018-09-03 17:22:44",
                        "updated_at": "2018-09-03 17:22:44"
                    }
                ]
            },
            "http://www.csindex.com.cn/uploads/file/autofile/perf/399702perf.xls",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/290_399702_Index_Methodology_cn.pdf",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/CSIMeth.pdf",
            "http://www.csindex.com.cn/uploads/file/autofile/cons/399702cons.xls",
            ""
        ],
        [
            {
                "index_id": 291,
                "index_code": "399703",
                "indx_sname": "深证F200",
                "index_ename": "SZFI 200",
                "base_point": "1000.0000",
                "base_date": "2002-12-31 00:00:00",
                "online_date": "2010-05-10",
                "is_custom": 0,
                "is_show": 1,
                "index_c_intro": "深证基本面200指数以深市A股为样本空间，分别挑选基本面价值最大的200家上市公司作为样本。基本面价值由四个财务指标来衡量，并决定了样本股的权重。",
                "index_e_intro": "SZFI 200 Index consists of top 200 SZSE-listed stocks ranked by fundamental value, which is calculated by 4 financial factors (Revenue, Cash Flow, Book Value and Dividends). And the weights of constituents are also decided by the fundamental value rather than the capitalization. ",
                "class_series": 3,
                "class_region": 7,
                "class_assets": 10,
                "class_classify": 21,
                "class_currency": 22,
                "class_hot": 25,
                "index_c_fullname": "深证基本面200指数",
                "index_e_fullname": "SZFI 200 Index",
                "created_at": "2017-07-03 14:00:02",
                "updated_at": "2017-07-03 14:00:02",
                "classes": {
                    "class_id": 3,
                    "class_type": 1,
                    "class_name": "深证系列指数",
                    "class_ename": "SZSE Indices",
                    "created_at": "2017-03-29 20:12:15",
                    "updated_at": "2017-03-29 20:12:23"
                },
                "files": [
                    {
                        "file_id": 1312,
                        "file_title": "编制方案",
                        "file_name": "291_399703_Index_Methodology_cn.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 1,
                        "index_id": 291,
                        "created_at": "2017-07-06 17:17:28",
                        "updated_at": "2017-07-06 17:17:28"
                    },
                    {
                        "file_id": 2829,
                        "file_title": "指数单张",
                        "file_name": "399703factsheet.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 2,
                        "index_id": 291,
                        "created_at": "2018-09-03 17:22:44",
                        "updated_at": "2018-09-03 17:22:44"
                    }
                ]
            },
            "http://www.csindex.com.cn/uploads/file/autofile/perf/399703perf.xls",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/291_399703_Index_Methodology_cn.pdf",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/CSIMeth.pdf",
            "http://www.csindex.com.cn/uploads/file/autofile/cons/399703cons.xls",
            ""
        ],
        [
            {
                "index_id": 292,
                "index_code": "399704",
                "indx_sname": "深证上游",
                "index_ename": "SZSE Upstream",
                "base_point": "1000.0000",
                "base_date": "2002-12-31 00:00:00",
                "online_date": "2011-10-18",
                "is_custom": 0,
                "is_show": 1,
                "index_c_intro": "深圳上游产业指数由深市A股中的上游资源产业公司股票组成样本股，以反映国民经济上游产业股票的整体表现。",
                "index_e_intro": "The SZSE Upstream Industry Index reflects the general performance of upstream industry stocks in Shenzhen market.",
                "class_series": 3,
                "class_region": 7,
                "class_assets": 10,
                "class_classify": 20,
                "class_currency": 22,
                "class_hot": "",
                "index_c_fullname": "深证上游产业指数",
                "index_e_fullname": "SZSE Upstream Industry Index",
                "created_at": "2017-07-03 14:00:02",
                "updated_at": "2017-07-03 14:00:02",
                "classes": {
                    "class_id": 3,
                    "class_type": 1,
                    "class_name": "深证系列指数",
                    "class_ename": "SZSE Indices",
                    "created_at": "2017-03-29 20:12:15",
                    "updated_at": "2017-03-29 20:12:23"
                },
                "files": [
                    {
                        "file_id": 1314,
                        "file_title": "编制方案",
                        "file_name": "292_399704_Index_Methodology_cn.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 1,
                        "index_id": 292,
                        "created_at": "2017-07-06 17:17:28",
                        "updated_at": "2017-07-06 17:17:28"
                    },
                    {
                        "file_id": 4522,
                        "file_title": "指数单张",
                        "file_name": "399704factsheet.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 2,
                        "index_id": 292,
                        "created_at": "2018-09-03 17:22:44",
                        "updated_at": "2018-09-03 17:22:44"
                    }
                ]
            },
            "http://www.csindex.com.cn/uploads/file/autofile/perf/399704perf.xls",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/292_399704_Index_Methodology_cn.pdf",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/CSIMeth.pdf",
            "http://www.csindex.com.cn/uploads/file/autofile/cons/399704cons.xls",
            ""
        ],
        [
            {
                "index_id": 293,
                "index_code": "399705",
                "indx_sname": "深证中游",
                "index_ename": "SZSE Midstream ",
                "base_point": "1000.0000",
                "base_date": "2002-12-31 00:00:00",
                "online_date": "2011-10-18",
                "is_custom": 0,
                "is_show": 1,
                "index_c_intro": "深圳中游产业指数由深市A股中的中游制造产业公司股票组成样本股，以反映国民经济中游产业股票的整体表现。",
                "index_e_intro": "The SZSE Midstream Industry Index reflects the general performance of midstream industry stocks in Shenzhen market.",
                "class_series": 3,
                "class_region": 7,
                "class_assets": 10,
                "class_classify": 20,
                "class_currency": 22,
                "class_hot": "",
                "index_c_fullname": "深证中游产业指数",
                "index_e_fullname": "SZSE Midstream Industry Index",
                "created_at": "2017-07-03 14:00:02",
                "updated_at": "2017-07-03 14:00:02",
                "classes": {
                    "class_id": 3,
                    "class_type": 1,
                    "class_name": "深证系列指数",
                    "class_ename": "SZSE Indices",
                    "created_at": "2017-03-29 20:12:15",
                    "updated_at": "2017-03-29 20:12:23"
                },
                "files": [
                    {
                        "file_id": 1316,
                        "file_title": "编制方案",
                        "file_name": "293_399705_Index_Methodology_cn.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 1,
                        "index_id": 293,
                        "created_at": "2017-07-06 17:17:28",
                        "updated_at": "2017-07-06 17:17:28"
                    },
                    {
                        "file_id": 4523,
                        "file_title": "指数单张",
                        "file_name": "399705factsheet.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 2,
                        "index_id": 293,
                        "created_at": "2018-09-03 17:22:44",
                        "updated_at": "2018-09-03 17:22:44"
                    }
                ]
            },
            "http://www.csindex.com.cn/uploads/file/autofile/perf/399705perf.xls",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/293_399705_Index_Methodology_cn.pdf",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/CSIMeth.pdf",
            "http://www.csindex.com.cn/uploads/file/autofile/cons/399705cons.xls",
            ""
        ],
        [
            {
                "index_id": 294,
                "index_code": "399706",
                "indx_sname": "深证下游",
                "index_ename": "SZSE Downstream",
                "base_point": "1000.0000",
                "base_date": "2002-12-31 00:00:00",
                "online_date": "2011-10-18",
                "is_custom": 0,
                "is_show": 1,
                "index_c_intro": "深圳下游产业指数由深市A股中的下游消费与服务产业公司股票组成样本股，以反映国民经济下游产业股票的整体表现。",
                "index_e_intro": "The SZSE Downstream Industry Index reflects the general performance of downstream industry stocks in Shenzhen market.",
                "class_series": 3,
                "class_region": 7,
                "class_assets": 10,
                "class_classify": 20,
                "class_currency": 22,
                "class_hot": "",
                "index_c_fullname": "深证下游产业指数",
                "index_e_fullname": "SZSE Downstream Industry Index",
                "created_at": "2017-07-03 14:00:02",
                "updated_at": "2017-07-03 14:00:02",
                "classes": {
                    "class_id": 3,
                    "class_type": 1,
                    "class_name": "深证系列指数",
                    "class_ename": "SZSE Indices",
                    "created_at": "2017-03-29 20:12:15",
                    "updated_at": "2017-03-29 20:12:23"
                },
                "files": [
                    {
                        "file_id": 1318,
                        "file_title": "编制方案",
                        "file_name": "294_399706_Index_Methodology_cn.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 1,
                        "index_id": 294,
                        "created_at": "2017-07-06 17:17:28",
                        "updated_at": "2017-07-06 17:17:28"
                    },
                    {
                        "file_id": 4524,
                        "file_title": "指数单张",
                        "file_name": "399706factsheet.pdf",
                        "file_type": "pdf",
                        "file_lang": 2,
                        "file_class": 2,
                        "index_id": 294,
                        "created_at": "2018-09-03 17:22:44",
                        "updated_at": "2018-09-03 17:22:44"
                    }
                ]
            },
            "http://www.csindex.com.cn/uploads/file/autofile/perf/399706perf.xls",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/294_399706_Index_Methodology_cn.pdf",
            "http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/CSIMeth.pdf",
            "http://www.csindex.com.cn/uploads/file/autofile/cons/399706cons.xls",
            ""
        ]
    ]
}
        
        
        ##################################################
        list =dict['list']
        for li in list:
            paramList = []
            index_id = ""
            index_code=""
            indx_sname=""
            index_ename=""
            base_point=""
            base_date=""
            online_date=" "
            index_c_intro=" "
            for item in li:
                #print(type(item))
                if type(item).__name__ == 'dict':
                    index_id = item['index_id']
                    index_code = item['index_code']
                    indx_sname = item['indx_sname']
                    index_ename= item['indx_sname'] 
                    base_point = item['base_point']
                    base_date = item['base_date']
                    online_date = item['online_date']
                    index_c_intro = item['index_c_intro']
            hangqingzoushi = li[1]+" "
            make_method = li[2]+" "
            weihuxize = li[3]+" "
            chengfenguliebiao = li[4]+" "
            type1=1
            type2=2
            type3=3
            
            paramList.append(str(index_id))
            paramList.append(index_code)
            paramList.append(indx_sname)
            paramList.append(index_ename)
            paramList.append(base_point)
            paramList.append(base_date)
            paramList.append(online_date)
            paramList.append(index_c_intro)
            paramList.append(hangqingzoushi)
            paramList.append(make_method)
            paramList.append(weihuxize)
            paramList.append(chengfenguliebiao)
            paramList.append(type3)
            
            #param = (index_id,index_code,indx_sname,index_ename,base_point,base_date,online_date,index_c_intro,hangqingzoushi,make_method,weihuxize,chengfenguliebiao,type1)
            print(paramList)
            insertSql = "INSERT INTO t_index_new(index_id,index_code,indx_sname,index_ename,base_point,base_date,online_date,index_c_intro,hangqingzoushi,make_method,weihuxize,chengfenguliebiao,agencyType) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE date_create = NOW() ON DUPLICATE KEY UPDATE remark =''"
            dbUtil = DBUtil("127.0.0.1",3306,"root","root","fund","utf-8")
            dbUtil.insert(insertSql, paramList)
            
if __name__=='__main__':
    indexSpider = IndexInfoSipder()
    indexSpider.getIndexInfo()