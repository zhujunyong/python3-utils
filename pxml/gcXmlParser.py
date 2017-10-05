#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''

Created on 2017.08.25
@author: zhujunyong

'''

import os
import sys
import time
import xml.etree.ElementTree as ET
import datetime



def parseXml(path):
    ns = {'ns':'http://www.ibm.com/j9/verbosegc'}
    tree = ET.parse(path)
    root = tree.getroot()

    content = ''
    for gcstart in root.findall('ns:gc-start',ns):
        timestamp = gcstart.attrib.get('timestamp')
        timestamp = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
        for meminfo in gcstart.findall('ns:mem-info',ns):
            for mem in meminfo.findall('ns:mem',ns):
                memType = mem.attrib.get('type')
                memFree = mem.attrib.get('free')
                memTotal = mem.attrib.get('total')
                memPercent = mem.attrib.get('percent')
                line = "%s,%s,%s,%s,%s\n" % (timestamp, memType, memFree, memTotal, memPercent)
                content += line
    return content


if __name__ == '__main__':
    #检查参数
    if len(sys.argv) < 2:
        print("usage: python3 gcXmlParser.py <xml file path>")
        print("for example : python3 nmonprocessor.py /Users/zhujunyong/Documents/git/python3-utils/pxml/gc.xml")
        sys.exit(0)
    #给路径赋值
    path = sys.argv[1]
    print("start parse %s..."  % path)
    content = parseXml(path)

    # if content == '', ignore it
    if len(content) == 0:
        print('no data')
        exit(0)

    fmtdFileName = path+'.formatted'
    # create or update .formatted file and append parsed content to it
    fmtdFile = open(fmtdFileName, 'w')
    try :
        fmtdFile.write(content)
    except Exception as err:
        print(err)
    finally:
        fmtdFile.close()

    print('write fmtd file:%s' % fmtdFileName)
