#! -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'User.views',
    url(r'^edit/$', 'edit', name='profile_edit'),
    url(r'^profile/(?P<tid>\d+)/$', 'view_profile', name='profile_view'),
    url(r'^info/(?P<tid>\d+)/$', 'view_info', name='info_view'),
    url(r'^base_info/$', 'base_info_edit', name='base_info_edit')
)
