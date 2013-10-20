#! -*- coding:utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'sys_notification.views',
    url(r'^notify/group/$', 'notify_group', name='notify_group'),
    url(r'^notify/topic/$', 'notity_topic', name='notify_topic'),
    url(r'^notify/del/$', 'del_notify', name='del_notify'),
)
