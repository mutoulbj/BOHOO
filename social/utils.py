#!/usr/bin/env python
#coding=utf-8
'''
Created on 2012-2-21

@author: Chine
'''

def count_words(content):
    if isinstance(content, str):
        content = content.decode('utf-8').encode('gbk')
    elif isinstance(content, unicode):
        content = content.encode('gbk')
        
    return float(len(content)) / 2

def get_twitter_content(content, size=140, span=0):
    result = ''
    rest_count = size
    for word in iter(content):
        rest_count -= count_words(word)
        if rest_count < span:
            break
        result += word
        
    return result