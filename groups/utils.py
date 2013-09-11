#! -*- coding:utf-8 -*-

from groups.models import Group


def get_groups(user):
    """ 根据用户返回其参加的所有群组 """
    return Group.objects.filter(member=user)
