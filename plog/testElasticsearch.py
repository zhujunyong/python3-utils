#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Created on 2017年5月5日
@author: zhujunyong
'''

from datetime import datetime
from elasticsearch import Elasticsearch


if __name__ == '__main__':
    es = Elasticsearch(hosts=[{'host':'192.168.100.232'}])
#    print(es.info())
    res = es.search(index="flume-2017-05-05", body={"query": {"match_all": {}}})
 
 
    print("Got %d Hits:" % res['hits']['total'])




