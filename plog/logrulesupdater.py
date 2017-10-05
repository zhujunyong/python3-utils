#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Created on 2017年5月9日
@author: zhujunyong
'''

from pymongo import MongoClient
from bson import ObjectId


# find in logAnalysis ,condition: result is not null, ruleId is not null
# return dict<ruleid,[correctCount, totalCount]>
def readLogAnalysis(conn):
    logAnalysis = conn.biglog.logAnalysis
    cursor = logAnalysis.find({'$and':[{'result':{'$exists':True}}, {'ruleid':{'$exists':True}}]})
    
    analysisDict = {}
    for row in cursor:
        ruleid = row['ruleid']
        result = row['result']
        # same as    correct = result ? 1 : 0
        correct = (result and 1) or 0

        if not ruleid in analysisDict :
            analysisDict[ruleid] = [0,0]
            
        analysisDict[ruleid][0] += correct    
        analysisDict[ruleid][1] += 1    

    cursor.close()
    return analysisDict
    
# update total accuracy rate in logRules    
def updateLogRuleAccuracy(conn, analysisDict):
    logRules = conn.biglog.logRules
    
    for k,v in analysisDict.items() :
        print('update ruleid:' + k + ', set correct='+str(v[0])+', total='+str(v[1]))
        logRules.update_one({'_id':ObjectId(k)}, {'$set':{'correct': v[0], 'total': v[1]}})



if __name__ == '__main__':
#    conn = MongoClient('192.168.100.232',27017)
    conn = MongoClient('node01',27017)
    analysisDict = readLogAnalysis(conn)
    updateLogRuleAccuracy(conn, analysisDict)

    
    conn.close()


