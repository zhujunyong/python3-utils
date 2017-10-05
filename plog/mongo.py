#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Created on 2017年5月4日
@author: zhujunyong
'''


import json
from pymongo import MongoClient


#read json file
def readFile(path):
    jsonfile = open(path)
    try:
        content = jsonfile.read()
    finally:
        jsonfile.close()
    return content

if __name__ == '__main__':
#    path = '/Users/zhujunyong/Documents/workspace/biglogweb/src/main/resources/common_relationship.json'
    path = '/Users/zhujunyong/Documents/workspace/biglogweb/src/main/resources/logRuleAccuracy.json'
    content = readFile(path)
#    print(content)
    jsonData = json.loads(content)
#    print(jsonData)
    
    conn = MongoClient('localhost',27017);
    collection = conn.biglog.logRuleAccuracy
    collection.insert(jsonData)
    
#    collection.remove({'system':'SSM'})
#    collection.remove({'system':'BIGLOG'})
#    row = collection.find_one()
#    print(row)
    


