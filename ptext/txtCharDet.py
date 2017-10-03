#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
analyse text file.
detect text content encodec
"""

__author__ = 'Zhu JunYong'

import sys
import os
import chardet

# read file content and detect the encoding
def detect(filename):
    # auto close file
    with open(filename, 'rb') as f:
        buf = f.read()
        result = chardet.detect(buf)
        codec = result['encoding']
        return codec

# program entrance, argv is text filename
if __name__ == '__main__':
    # check argv
    if len(sys.argv) < 2:
        print("usage: python3 txtCharDet.py filename")
        print("filename: the text file name which you want to detect codec.")
        sys.exit(0)
    filename = sys.argv[1]
    # check file exists or not
    if not os.path.exists(filename):
        print("the file does not exists.")
        sys.exit(0)

    codec = detect(filename)
    print(codec)
