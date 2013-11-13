#! -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
                       url(r'^login/$', 'login', name='login'),
                       url(r'^register/$', 'register', name='register'),
                       url(r'^logout/$', 'log_out', name='logout'),
                       url(r'^reset_password_apply/$', 'reset_password_apply', name='reset_password_apply'),
                       url(r'^reset_password/(?P<user_id>\d+)/$', 'reset_password', name='reset_password'),
                       url(r'^username_check/$', 'username_check', name='username_check'),
                       url(r'^email_check/$', 'email_check', name='email_check'),
                       )