#! -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'User.views',
    url(r'^edit/$', 'edit', name='profile_edit'),
    url(r'^profile/(?P<tid>\d+)/$', 'view_profile', name='profile_view'),
    url(r'^info/(?P<tid>\d+)/$', 'view_info', name='info_view'),
    url(r'^info/add_topic/(?P<tid>\d+)/$', 'm_add_topic', name='m_add_topic'),
    url(r'^info/reply_topic/(?P<tid>\d+)/$', 'm_reply_topic', name='m_reply_topic'),
    url(r'^base_info/$', 'base_info_edit', name='base_info_edit')
)
