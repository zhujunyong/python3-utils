#!/usr/bin/env python3
# -*- coding: utf8 -*-



import sys
import xml.etree.ElementTree as ET
from elasticsearch import Elasticsearch
import re
import datetime
import time




if __name__ == '__main__':
    esserver = 'node01'
    esindex='knowledge'
    estype='wikipedia'
    #------ end argv -----------

    # connect to es server
    es = Elasticsearch(esserver)
    # create index
    es.indices.create(index=esindex,ignore=400)
#    res = es.get(index=esindex, doc_type=estype)
    res = es.search(index=esindex, doc_type=estype, body={"query":{"match":{"language":"en"}}})

    print(res)
    print(type(res))
