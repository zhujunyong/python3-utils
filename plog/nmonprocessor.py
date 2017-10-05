#!/usr/bin/env python3
# -*- coding: utf8 -*-

'''

Created on 2017年5月22日
@author: zhujunyong

log path example:
/logpath/hostname/nmon/*.nmon

/logpath is input argv

dependence following libs:
    # nmonvisualizer.jar
    # jackson-annotations-2.7.1.jar
    # jackson-databind-2.7.1-1.jar
    # jfreechart-1.0.19.jar
    # slf4j-api-1.7.16.jar
    # jackson-core-2.7.1.jar
    # jcommon-1.0.23.jar
    # slf4j-jdk14-1.7.16.jar

    tested on nmon16e & 16g

'''

import os
import sys
import time
import jpype


# 解析指定的xxx.nmon文件
# filename: nmon文件名
# maxTimestamp: nmon解析结果中时间戳大于此值的记录才返回（小于此值说明之前已经解析过了）
def parseNmonFile(filename, maxTimestamp):
    print('parse  nmon file:%s' % filename)

    # init nmon DataSet
    Calendar = jpype.JClass('java.util.Calendar')
    NMONParser = jpype.JClass('com.ibm.nmon.parser.NMONParser')
    ds = NMONParser().parse(filename, Calendar.getInstance().getTimeZone(), True);
    # init nmon DataType
    DataType = jpype.JClass('com.ibm.nmon.data.DataType')
    # init Java String Array
    Array = jpype.JArray(jpype.JString)(1)

    diskbsizeIndex = 0
    diskreadIndex = 0
    diskwriteIndex = 0
    diskxferIndex = 0
    fsList = []
    # get index value
    for dt in ds.getTypes():
        if dt.getId() == 'DISKBSIZE':
            diskbsizeIndex = dt.getFieldIndex("Total")
        if dt.getId() == 'DISKREAD':
            diskreadIndex = dt.getFieldIndex("Total")
        if dt.getId() == 'DISKWRITE':
            diskwriteIndex = dt.getFieldIndex("Total")
        if dt.getId() == 'DISKXFER':
            diskxferIndex = dt.getFieldIndex("Total")
        if dt.getId() == 'JFSFILE':
            fsList = dt.getFields()


    # parse nmon data
    content = ''
    for dr in ds.getRecords():
        # cpu,mem,disk,network line
        line = ''
        # ignore formatted content
        if dr.getTime() <= maxTimestamp :
            continue
        #timestamp 1
        line += '%d,' % dr.getTime()
        # filesystem line ,timestamp string prefix
        timestamps = line
        #cpu_all: 7 items
        for d in dr.getData(DataType('CPU_ALL', 'CPU_ALL', Array)):
            line += '%.1f,' % d
        #mem: 16 items
        for d in dr.getData(DataType('MEM', 'MEM', Array)):
            line += '%.1f,' % d
        #net: 6 items
        for d in dr.getData(DataType('NETETOTAL', 'NETETOTAL', Array)):
            line += '%.1f,' % d
        #disk: 4 items
        line += '%.1f,' % dr.getData(DataType('DISKBSIZE', 'DISKBSIZE', Array))[diskbsizeIndex]
        line += '%.1f,' % dr.getData(DataType('DISKREAD', 'DISKREAD', Array))[diskreadIndex]
        line += '%.1f,' % dr.getData(DataType('DISKWRITE', 'DISKWRITE', Array))[diskwriteIndex]
        line += '%.1f,' % dr.getData(DataType('DISKXFER', 'DISKXFER', Array))[diskxferIndex]


        #firesystem output file
        fsUsedArray = dr.getData(DataType('JFSFILE', 'JFSFILE', Array))
        processedArray = []
        for i in range(0, len(fsList)):
            # 这段if else是为了去重复，nmonvisualizer不知为何有时会把 / 解析出两个一样的来
            if fsList[i] in processedArray:
                continue
            else:
                processedArray.append(fsList[i])

            flag = '#' if (i < len(fsList) - 1) else '\n'
            # 输出格式为 文件系统路径一#used%|文件系统路径二#used%|文件系统路径三#used%|
            # for example:   /:16.0#/dev:0.0#/run:0.7#/dev/hugepages:0.0#/dev/mqueue:0.0#/boot:17.0#/home:17.3#/run/user/42:0.0#/run/user/0:0.0#/cdrom:100.0
            line += '%s:%.1f%s' % (fsList[i], fsUsedArray[i], flag)

        #append line to content
        content += line

    return content


# 遍历目录，找出所有的.nmon文件，并对每一个(符合条件的)文件调用解析方法 parseNmonFile()
# 然后把解析出的内容追加到.formatted文件中.
# path:需要遍历的目录
# offset:限制时间的时间戳，时间戳以内更新的nmon文件才解析，默认无限制
def loopPath(path, offset = -1):
    for hostname in os.listdir(path):
        nmonPath = path + hostname + '/nmon/'

        # ignore invalid path
        if not os.path.isdir(nmonPath) :
            continue
        # process nmon file
        for f in os.listdir(nmonPath) :
            if not os.path.splitext(f)[1] == '.nmon':
                continue
            nmonFileName = nmonPath + f
            # 如果设定了限制时间，例如只检查10分钟内更新过的文件，则比较文件的修改时间
            if offset > 0 and os.path.getmtime(nmonFileName) < offset :
                continue

            fmtdFileName = os.path.splitext(nmonFileName)[0]+'.formatted'
            fsFileName = os.path.splitext(nmonFileName)[0]+'.jfsfile'
            maxTimestamp = queryMaxTimestampInFormattedFile(fmtdFileName)
            # parse nmon file
            content = parseNmonFile(nmonFileName, maxTimestamp)
            # if content == '', ignore it
            if len(content) == 0:
                continue

            # create or update .formatted file and append parsed content to it
            fmtdFile = open(fmtdFileName, 'a')
            try :
                fmtdFile.write(content)
            except Exception as err:
                print(err)
            finally:
                fmtdFile.close()

            print('update fmtd file:%s' % fmtdFileName)
            # remove old parsed nmon file
            # os.remove(fullFileName)



# 获取formatted文件的最大时间戳，以便于解析nmon文件时可以过滤掉已经解析过的内容
# 获取该文件的最后一行取出时间戳即可
def queryMaxTimestampInFormattedFile(fmtdFileName):
    if not os.path.exists(fmtdFileName) :
        return 0
    f = os.popen('tail -n 1 %s' % fmtdFileName)
    maxTimestamp = 0
    try :
        maxTimestamp = int(f.readline().split(',')[0])
    except Exception as err:
        print(err)
    finally:
        f.close()
    return maxTimestamp


if __name__ == '__main__':
    #libpath = '/Users/zhujunyong/Downloads/nmontest/libs'
    #path = '/Users/zhujunyong/Downloads/nmontest'
    #检查参数
    if len(sys.argv) < 3:
        print("usage: python3 nmonprocessor.py <nmonpath> <libpath> <minutes(optional)>")
        print("nmonpath: the nmon file path that you want to process")
        print("libpath : the nmonvisualizer jars path")
        print("minutes : only check recently '*.nmon' files to reduce cost, if no specify this argu, it will check all nmon files")
        print("for example : python3 nmonprocessor.py /var/log /home/platform/biglog/python3-script/libs 10")
        sys.exit(0)
    #给路径赋值
    path = sys.argv[1]
    libpath = sys.argv[2]
    #检查路径是否合法
    if not os.path.isdir(path):
        print("the directory:%s is not a path or does not exist" % path)
        sys.exit(0)
    if not os.path.isdir(libpath):
        print("the directory:%s is not a path or does not exist" % libpath)
        sys.exit(0)

    if not path.endswith('/'):
        path = path + '/'
    # 如果用户输入了检查时间的限制参数，则需要计算检查时间的时间戳
    offset = -1
    if len(sys.argv) >= 4 :
        minutes = int(sys.argv[3])
        offset = time.time() - (minutes * 60)

    # startup jvm
    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % libpath)
    loopPath(path, offset)
    # shutdown jvm
    jpype.shutdownJVM()
