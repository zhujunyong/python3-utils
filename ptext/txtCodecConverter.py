#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
analyse text file.
save specified file as target codec
"""

__author__ = 'Zhu JunYong'

import sys
import os
import txtCharDet

def readFileContent(filename, codec):
    with open(filename, 'r', encoding=codec) as f:
        content = f.read()
        return content

def saveContent(filename, content, codec):
    with open(filename, 'w', encoding=codec) as f:
        f.write(content)



# program entrance, argv is text filename & target codec
if __name__ == '__main__':
    # check argv
    if len(sys.argv) < 3:
        print("usage: python3 txtCodecConverter.py sourceFilename targetCodec")
        print("sourceFilename: the text file name which you want to read.")
        print("targetCodec: the target codec which you want to save as...")
        sys.exit(0)
    filename = sys.argv[1]
    targetCodec = sys.argv[2]
    # check file exists or not
    if not os.path.exists(filename):
        print("the file does not exists.")
        sys.exit(0)

    # get source codec of filename
    sourceCodec = txtCharDet.detect(filename)
    print('source codec is %s' % sourceCodec)

    # read content of filename
    content = readFileContent(filename, sourceCodec)

    # save content as targetCodec in new filename
    newfilename = filename+'.formatted'
    saveContent(newfilename, content, targetCodec)

    print('done')
