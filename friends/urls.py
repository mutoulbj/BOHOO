#! -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    "friends.views",
    url(r'^follow/(?P<user_id>\d+)/$', 'follow', name='friend_follow'),
)