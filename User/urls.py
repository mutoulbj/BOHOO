#! -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'User.views',
    url(r'^edit/$', 'edit', name='profile_edit'),
)
