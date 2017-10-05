#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''

Created on 2017.09.27
@author: zhujunyong

'''

import os
import sys
import time
import datetime



def parseLog(path):
    mylist=[]
    for line in open(path):
        line = line.replace('HMC [','$')
        line = line.replace('] failed!','')
        item = line.split('$')
        if item[1] not in mylist:
            mylist.append(item[1])

    mylist.sort()

    content = ''
    for i in mylist:
        content += i


    print(content)
    return content



if __name__ == '__main__':
    #检查参数
    if len(sys.argv) < 2:
        print("usage: python3 bocomGrepBadHmc.py <file path>")
        print("for example : python3 bocomGrepBadHmc.py /Users/zhujunyong/Downloads/errorhmc")
        sys.exit(0)
    #给路径赋值
    path = sys.argv[1]
    print("start parse %s..."  % path)
    content = parseLog(path)

    # if content == '', ignore it
    if len(content) == 0:
        print('no data')
        exit(0)

    fmtdFileName = path+'.txt'
    # create or update .formatted file and append parsed content to it
    fmtdFile = open(fmtdFileName, 'w')
    try :
        fmtdFile.write(content)
    except Exception as err:
        print(err)
    finally:
        fmtdFile.close()

    print('write fmtd file:%s' % fmtdFileName)
