#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Created on 2017年5月9日
@author: zhujunyong
'''

from pymongo import MongoClient
import datetime


# find in logAnalysis ,condition: result is not null, ruleId is not null
# return dict<ruleid,[correctCount, totalCount]>
def readLogAnalysis(conn, myday):
    logAnalysis = conn.biglog.logAnalysis
    key = '^'+myday+".*"
    cursor = logAnalysis.find({'$and':[{'result':{'$exists':True}}, {'ruleid':{'$exists':True}},{'createdate':{'$regex':key}}]})

#    print(myday + ':'+ str(cursor.count()))

    #dict<ruleid,[correctCount, totalCount]>
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
def updateLogRuleAccuracy(conn, analysisDict, myday):
    logRuleAccuracy = conn.biglog.logRuleAccuracy

    for k,v in analysisDict.items() :
#        print("k="+k+","+str(v))
        row = logRuleAccuracy.find_one({'$and':[{"createdate":myday},{"ruleid":k}]})
#        print("row="+str(row))
        if row == None:
            #insert
            print('insert into logRuleAccuracy. createdate:'+myday+',ruleid:'+k+',correct:'+str(v[0])+',total:'+str(v[1]))
            logRuleAccuracy.insert_one({'createdate':myday,'ruleid':k,'correct':v[0],'total':v[1]})
        else:
            #update
            print('update logRuleAccuracy. createdate:'+myday+',ruleid:'+k+',correct:'+str(v[0])+',total:'+str(v[1]))
            logRuleAccuracy.update_one({'$and':[{"createdate":myday},{"ruleid":k}]}, {'$set':{'correct': v[0], 'total': v[1]}})


if __name__ == '__main__':
    # 做几天的统计，1表示只做今天，2表示做今天和昨天，以此类推
    mydays = 32
    # 生成日期字符串列表
    now = datetime.date.today()
    mylist = [ str(now - datetime.timedelta(days=i)) for i in range(0, mydays) ]
#    print(mylist)

    # 连上mongodb
    conn = MongoClient('node01',27017)
#    conn = MongoClient('192.168.100.232',27017)
    # 根据日期做循环，从当天开始往前循环
    for myday in mylist:
        # 找出这一天的ruleid，正确数和总数的对应关系
        analysisDict = readLogAnalysis(conn, myday)
        # 按日期更新logRuleAccuracy
        updateLogRuleAccuracy(conn, analysisDict, myday)


    conn.close()
