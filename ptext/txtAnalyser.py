#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
analyse text file.
split words and count it by jieba
"""

__author__ = 'Zhu JunYong'

import sys
import os
import jieba
import jieba.posseg as pseg

#遍历指定路径去寻找符合targets条件的文件或文件夹
def analyse(source, target):
    print("source:%s, target:%s" % (source, target))
    dic = {}
    with open(source) as sourceFile:
        for line in sourceFile:
            seg = jieba.cut(line.strip(), cut_all = False)
            for item in seg:
                if (item in dic):
                    dic[item] = dic[item] + 1
                else:
                    dic[item] = 1
    for key, value in dic.items():
        if (value > 1000):
            print('key %s , value %d' % (key, value))


#程序入口
if __name__ == '__main__':
    #检查参数
    if len(sys.argv) < 2:
        print("usage: python3 txtAnalyser.py filename")
        print("filename: the text file name which you want to analyse it.")
        sys.exit(0)
    #给路径和检查列表赋值
    filename = sys.argv[1]

    if not os.path.exists(filename):
        print("the file does not exist.")
        sys.exit(0)

    newfilename = filename + '.cutted'

    analyse(filename, newfilename)
