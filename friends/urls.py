#! -*- coding:utf-8 -*-
'''
Created on 2013年8月12日

@author: amaozhao
'''
from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from friends.views import myfollow, myfans, action, userfollow, userfans

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/relation/myfollow/')),
    url(r'^myfollow/$', myfollow, name='myfollow'),
    url(r'^myfans/$', myfans, name='myfans'),
    
    #查看非登陆用户的好友关系
    url(r'^(?P<user_id>[\d]+)/follow/$', userfollow, name='uerfollow'),
    url(r'^(?P<user_id>[\d]+)/fans/$', userfans, name='userfans'),
    
    #关注和取消关注的操作
    url(r'^action/$', action, name='action'),
)
