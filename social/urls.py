#!/usr/bin/env python
#coding=utf-8
'''
Created on 2012-1-28

@author: Chine
'''

from django.conf.urls import patterns, url

urlpatterns = patterns('social.views',
    url(r'^logout/$', 'logout', name='social_logout')
)

urlpatterns += patterns('social.views',
    url(r'^google/login/$', 'google_login', name='social_google_login'),
    url(r'^google/login/done/$', 'google_auth', name='social_google_login_done'),
)

urlpatterns += patterns('social.views',
    url(r'^weibo/login/$', 'weibo_login', name='social_weibo_login'),
    url(r'^weibo/login/done/$', 'weibo_auth', name='social_weibo_login_done')
)

urlpatterns += patterns('social.views',
    url(r'^renren/login/$', 'renren_login', name='social_renren_login'),
    url(r'^renren/login/done/$', 'renren_auth', name='social_renren_login_done')
)

urlpatterns += patterns('social.views',
    url(r'^qqweibo/login/$', 'qqweibo_login', name='social_qqweibo_login'),
    url(r'^qqweibo/login/done/$', 'qqweibo_auth', name='social_qqweibo_login_done')
)