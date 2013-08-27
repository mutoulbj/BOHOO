#!/usr/bin/env python
#coding=utf-8
'''
Created on 2012-2-21

@author: Chine
'''

from weibo import client as weibo_client
from txweibo import client as tx_client
from renren import client as renren_client
from utils import get_twitter_content

class MixedClient(object):
    @classmethod
    def update_status(cls, content):
        content = get_twitter_content(content)
        
        for c in (weibo_client, tx_client, renren_client):
            c.update_status(content)