#! -*- coding:utf-8 -*-
from friends.models import Friendship


def get_followers(user=None):
    """根据用户对象获取所有粉丝 返回queryset  @fanlintao 20131105"""
    return Friendship.objects.filter(to_user=user)


def get_followed(user=None):
    """根据用户对象获取所有关注的人 返回queryset @fanlintao 20131105"""
    return Friendship.objects.filter(from_user=user)
