#! -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^register/$', 'register', name='register'),
    url(r'^logout/$', 'log_out', name='logout'),
    url(r'^view_member_info/$', 'view_member_info', name='view_member_info'),
    url(r'^username_check/$', 'username_check', name='username_check'),
    url(r'^email_check/$', 'email_check', name='email_check'),
)