#! -*- coding:utf-8 -*-
'''
Created on 2013年8月12日

@author: amaozhao
'''
from django.conf.urls import patterns, url

from friends.views import following, followed, action

urlpatterns = patterns('',
    url(r'^following/$', following, name='following'),
    url(r'^followed/$', followed, name='followed'),
    url(r'^action/$', action, name='action'),
)
