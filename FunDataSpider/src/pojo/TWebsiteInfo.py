#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TWebsiteInfo(object):
    
    def __init__(self,id,item_name,item_url,type,level,date_create,date_update,parent_id):
        self.id =id
        self.item_name = item_name
        self.item_url = item_url
        self.type = type
        self.level = level
        self.date_create = date_create
        self.date_update = date_update
        self.parent_id=parent_id
        
    
    def toString(self):
        print('[TWebsiteInfo]:id:%s ,item_name:%s ,item_url:%s ,type:%s ,level:%s ,date_create:%s ,date_update:%s ' % (self.id,self.item_name,self.item_url,self.type,self.level,self.date_create,self.date_update))

if __name__=='__main__':
    aa = TWebsiteInfo(1,'aa','bb','bb','bb','bb','bb')
    aa.toString()