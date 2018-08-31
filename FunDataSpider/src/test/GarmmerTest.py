#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from lxml import etree
from statsmodels.discrete.tests.test_sandwich_cov import filepath

class GrammerTest(object):
    def __init__(self):
        pass
    
    def readFile(self,filePath):
        try:
            doc = pq(filePath)
            print(doc)
        except Exception as e:
            print(e.reason)

if __name__ == '__main__':
    grammerTest = GrammerTest()
    grammerTest("../../../../htmls/home.html")