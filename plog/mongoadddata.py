#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Created on 2017年5月4日
@author: zhujunyong
'''


import json
from pymongo import MongoClient
from bson import ObjectId
import random

def test(collection):
    mylist = ['58db5ec7d08eaa5bbed59381','58db5ec7d08eaa5bbed59386']
    cursor = collection.find({"ruleid":{"$exists":False}})
    for row in cursor:
        print(row)
        i = random.random()
        if i > 0.5 :
            i = 1
        else:
            i = 0
        collection.update_one({"_id":row['_id']},{'$set':{ "ruleid": mylist[i]}})
#        print(i)

if __name__ == '__main__':

    
#    conn = MongoClient('192.168.100.232',27017);
    conn = MongoClient('localhost',27017);
    collection = conn.biglog.logAnalysis
    test(collection)
#    collection.insert(jsonData)
    
#    collection.remove({'system':'SSM'})
#    collection.remove({'system':'BIGLOG'})
#    row = collection.find_one()
#    print(row)
    


