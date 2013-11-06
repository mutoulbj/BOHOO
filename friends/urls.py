#! -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    "friends.views",
    url(r'^follow/(?P<user_id>\d+)/$', 'follow', name='friend_follow'),
    url(r'^friend_tooltip/$', 'friend_tooltip', name='friend_tooltip'),
    url(r'^follow/$', 'ajax_follow', name='ajax_follow'),
    url(r'^unfollow/$', 'ajax_unfollow', name='ajax_unfollow'),
)