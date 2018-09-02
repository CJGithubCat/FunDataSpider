#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Title  :     
Date :   2018年9月2日
Version:  1.0
'''
class TFundSummary(object):
    def __init__(self,fund_code,fund_name,buy_status,redemption_status,poundage,fund_type,trace_type,trace_target,index_id,detail_url):
        self.fund_code=fund_code
        self.fund_name=fund_name
        self.buy_status=buy_status
        self.redemption_status=redemption_status
        self.poundage=poundage
        self.fund_type=fund_type
        self.trace_type=trace_type
        self.trace_target=trace_target
        self.index_id=index_id
        self.detail_url=detail_url
    
    def toString(self):
        print('[TFundSummary]self:%s ,fund_code:%s ,fund_name:%s ,buy_status:%s ,redemption_status:%s ,poundage:%s ,fund_type:%s ,trace_type:%s ,trace_target:%s ,index_id:%s ,detail_url:%s ' % (self.fund_code,self.fund_name,self.buy_status,self.redemption_status,self.poundage,self.fund_type,self.fund_type,self.trace_type,self.trace_target,self.index_id,self.detail_url))
        