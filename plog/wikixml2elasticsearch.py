#!/usr/bin/env python3
# -*- coding: utf8 -*-



import sys
import xml.etree.ElementTree as ET
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import re
import datetime
import time

# return dict
def getMeta(line):
    line += '</doc>'
    root = ET.fromstring(line)
    return root.attrib

# insert data into elasticsearch
def putData(id, url, title, content, es, esindex, estype):
    #print("id     :%d" % int(id))
    #print("url    :%s" % url)
    #print("title  :%s" % title)
    #print("content:%s" % content)

    data={
        'id':id,
        'url':url,
        'title':title,
        'content':content
        #'language':'en'
    }
    #es.index(index=esindex, doc_type=estype, body=data )
    result = {"_index":esindex, "_type":estype, "_source":data}
    return result

def bulk(es, actions, esindex):
    try:
        helpers.bulk(es, actions, index=esindex)
    except Exception as e:
        print(e)

if __name__ == '__main__':
#    '<doc id="21" url="https://zh.wikipedia.org/wiki?curid=21" title="文學">'

    #------ begin argv -----------
    #filename = '/Users/zhujunyong/Downloads/wiki_00'
    #filename = '/Users/zhujunyong/Downloads/wiki.xml'
    #filename = '/tmp/wiki.xml'
    filename = '/data/enwiki.xml'
    esserver = 'node01'
    esindex='enwiki'
    estype='doc'
    batchsize=1000
    #------ end argv -----------

    # connect to es server
    es = Elasticsearch(esserver, timeout=5000)
    # create index
    es.indices.create(index=esindex,ignore=400)

    doc_begin = r'^<doc id="\d+" +url=".*" +title=".*">$'
    doc_end   = r'</doc>'

    title = None
    url = None
    id = None
    content = ''
    actions = []
    looptimes = 0
    f = open(filename)
    for line in f:
        if (len(actions) >= batchsize):
            bulk(es, actions, esindex)
            looptimes += 1
            print("total %d records processed" % (batchsize * looptimes) )
            sys.stdout.flush()
            actions=[]

        doc_prefix = re.match(doc_begin, line)
        # 文章开头
        if (doc_prefix != None):
            meta = getMeta(line)
            id = int(meta['id'])
            url = meta['url']
            title = meta['title']
            content = ''
            continue

        # 文章结束
        if doc_end in line:
            result = putData(id, url, title, content, es, esindex, estype)
            actions.append(result)
            #print(len(actions))
            continue

        # 正文
        content += line

    f.close()

    if (len(actions) > 0):
        bulk(es, actions, esindex)
        print("total %d records processed" % (batchsize * looptimes + len(actions)) )

    print('done')
